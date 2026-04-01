import typing

from BaseClasses import Item, Tutorial, ItemClassification, Region, MultiWorld, CollectionState,Entrance,Location
from rule_builder.rules import *
from rule_builder.cached_world import CachedRuleBuilderWorld
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, World
from Options import OptionError
from .Items import OSRSMItem, starting_area_dict, chunksanity_starting_chunks, QP_Items, ItemRow, \
    chunksanity_special_region_names, OSRSMTrainingItem, OSRSMQuestPointItem, OSRSMKudosItem, OSRSMCombatPointsItem
from .Locations import OSRSMLocation
from .Rules import *
from .Options import OSRSMOptions, StartingArea
from .Names import LocationNames, ItemNames, RegionNames
from Utils import visualize_regions
from Options import OptionError

from .LogicCSV.LogicCSVToPython import data_csv_tag
#from .LogicCSV.items_generated import item_rows
#from .LogicCSV.locations_generated import location_rows
#from .LogicCSV.regions_generated import region_rows
#from .LogicCSV.resources_generated import resource_rows
from .LogicCSV.regions_generated2 import region_rows,resource_rows
from .LogicCSV.items_generated2 import item_rows, rollable_chunks
from .LogicCSV.locations_generated2 import location_rows, sub_quests, quests, non_quests, training_methods
from .LogicCSV.entrances_generated2 import rr_entrances,re_entrances,ee_entrances,rm_entrances,me_entrances, mm_entrances
from .LogicCSV.monsters_generated2 import monster_drops, non_monster_drops
from .LogicCSV.macros_generated2 import skill_names, task_macros
from .Regions import RegionRow, ResourceRow, DropElement, MonsterRow, RuleElement, RewardElement, LocationRow, EntranceRow, TrainingRow

from typing import Callable, Counter
import logging

logger = logging.getLogger(__name__)
class OSRSMWeb(WebWorld):
    theme = "stone"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Old School Runescape Randomizer connected to an Archipelago Multiworld for Members logic",
        "English",
        "setup_en.md",
        "setup/en",
        ["digiholic","Faris"]
    )
    tutorials = [setup_en]

base_id = 0x070000


def _make_rule_builder_item_mapping() -> dict[str, str]:
    """Rule Builder's item_mapping allows collected/removed items to tell Rule Builder's caching that they update a
    particular cached item or pseudo-item that rules may check for."""
    item_mapping: dict[str, str] = {}

    # Training
    for skill_name in skill_names:
        map_from = [f"Training_{skill_name}_{level}" for level in range(1, 100)]
        map_to = f"Training_{skill_name}"
        item_mapping.update(dict.fromkeys(map_from, map_to))

    # Quest Points, Kudos and Combat Points
    for location_rows_list in [location_rows, sub_quests]:
        for location_row in location_rows_list:
            if location_row.quest_point_reward > 0:
                item_mapping[f"QP {location_row.quest_point_reward} ({location_row.name})"] = "Quest Point"
            if location_row.kudos_reward > 0:
                item_mapping[f"Kudos {location_row.kudos_reward} ({location_row.name})"] = "Kudo"
            if location_row.combat_point_reward > 0:
                item_mapping[f"CombatPoints {location_row.combat_point_reward} ({location_row.name})"] = "Combat Point"

    return item_mapping


class OSRSMWorld(CachedRuleBuilderWorld):
    """
    The best retro fantasy MMORPG on the planet. Old School is RuneScape but… older! This is the open world you know and love, but as it was in 2007.
    The Randomizer takes the form of a Chunk-Restricted members Ironman that takes a brand new account up through whatever task you want to assign
    your self as a goal!
    """

    game = "Old School Runescape Members"
    options_dataclass = OSRSMOptions
    options: OSRSMOptions
    topology_present = True
    web = OSRSMWeb()
    base_id = base_id
    data_version = 1
    rule_caching_enabled = True

    location_rows_by_category:dict[str,list[LocationRow]] = {}
    for location_row in location_rows:
        if location_row.category not in location_rows_by_category:
            location_rows_by_category[location_row.category] = []
        location_rows_by_category[location_row.category].append(location_row)

    item_name_to_id = {item_rows[i].name: base_id + i for i in range(len(item_rows))}
    location_name_to_id = {location_rows[i].name: base_id + i for i in range(len(location_rows))}
    item_mapping = _make_rule_builder_item_mapping()
    item_name_groups = { macro_name: set(item_list) for macro_name, item_list in rollable_chunks.items()}
    location_name_groups = { category : set([location_row.name for location_row in location_rs]) for category, location_rs in location_rows_by_category.items()}

    item_rows_by_name: typing.ClassVar[dict[str, ItemRow]] = {it_row.name: it_row for it_row in item_rows}
    location_name_to_row: ClassVar[dict[str,LocationRow]] = {loc_row.name:loc_row for loc_row in (location_rows+sub_quests)}
    region_code_to_name: ClassVar[dict[str,str]] = {reg_row.id:reg_row.name for reg_row in region_rows}


    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.region_name_to_data: typing.Dict[str, Region] = {}
        self.location_name_to_data: typing.Dict[str, OSRSMLocation] = {}
        self.training_to_data: typing.Dict[str, OSRSMLocation] = {}
        self.training_to_row: typing.Dict[str, TrainingRow] = {}

        self.starting_area_item = ""

        self.available_QP_locations: typing.List[str] = []
        self.pre_completed_locations = []
        self.items_already_created = 0

    def generate_early(self) -> None:

        if getattr(self.multiworld,"generation_is_fake",False):
            self.options.disable_chunk_culling.value = True #don't cull in UT, this is fine because UT doens't do fill
            self.options.disable_task_culling.value = True 

        if self.options.starting_area.value in rollable_chunks:
            self.starting_area_item = self.random.choice(rollable_chunks[self.options.starting_area.value])
        else:
            starting_area_name = f"Area: {self.options.starting_area.value}"

            self.starting_area_item = starting_area_name if starting_area_name in self.item_name_to_id else "Area: Lumbridge Castle"

        defered_banned_chunks:set[str] = set()
        region_codes = self.region_code_to_name.keys()
        for chunk_id in self.options.banned_chunks:
            if chunk_id not in region_codes:
                defered_banned_chunks |= {code for code in region_codes if (chunk_id+"-") in code}
        self.options.banned_chunks.value |= defered_banned_chunks

        self.multiworld.push_precollected(self.create_item(self.starting_area_item))

        partial_names = []
        for loc_name in self.options.pre_completed_tasks.value:
            if "Complete the" in loc_name:
                loc_name,_ = loc_name.split(" Complete the",2) #Get just the name of the diary/quest
                partial_names.append(loc_name) #we're going to look for them later
            elif loc_name in self.location_name_groups:
                for sub_loc_name in self.location_name_groups[loc_name]:
                    if "Complete the" in loc_name:
                        loc_name,_ = loc_name.split(" Complete the",2) #Get just the name of the diary/quest
                        partial_names.append(loc_name) #we're going to look for them later
                    self.pre_completed_locations.append(sub_loc_name)
            else:
                self.pre_completed_locations.append(loc_name) #if it's not something with sub-tasks, just add it directly
        for loc_name in self.location_name_to_row.keys():
            if any(part_name in loc_name for part_name in partial_names):
                self.pre_completed_locations.append(loc_name)

    """
    This function pulls from LogicCSVToPython so that it sends the correct tag of the repository to the client.
    _Make sure to update that value whenever the CSVs change!_
    """

    def fill_slot_data(self):
        data = self.options.as_dict("brutal_grinds")
        data["data_csv_tag"] = data_csv_tag
        data["starting_area"] = str(self.starting_area_item) #these aren't actually strings, they just play them on tv
        data["goal_task"] = self.options.goal_location.value
        return data

    def explain_rule(self, dest_name: str, state: CollectionState):
        dest_name = dest_name.lower()
        if dest_name in [skill.lower() for skill in skill_names]:
            if dest_name in ("attack","strength","defence","prayer","hitpoints","combat","hp"):
                if state.can_reach_region("kill_Monster[+]",self.player):
                    return [{"type":"text","text": f"Standard combat skill to level {1+(state.count('Quest Point',self.player)//2)}"}]
                else:
                    return [{"type":"text","text":"Standard combat skill, but no monster to kill to level"}]
            elif dest_name == "slayer":
                if state.can_reach_region("PointSlayerMasters[+]",self.player):
                    return [{"type":"text","text": f"Slayer skill to level {1+(state.count('Quest Point',self.player)//2)}"}]
                else:
                    return [{"type":"text","text":"Slayer skill, but no master to get tasks"}]
            elif dest_name == "ranged":
                if state.can_reach_region("kill_Monster[+]",self.player) and state.can_reach_region("Iron arrow",self.player):
                    return [{"type":"text","text": f"Standard combat skill to level {1+(state.count('Quest Point',self.player)//2)}"}]
                else:
                    return [{"type":"text","text":"Standard combat skill, but no monster to kill to level (or no iron arrows)"}]
            else:
                relevent_methods = sorted([method_name for method_name,method in self.training_to_row.items() if method.skill_name.lower() == dest_name and self.training_to_data[method_name].can_reach(state)],key=lambda method_name: self.training_to_row[method_name].required_level)
                return_list = []
                delta_level = self.options.base_training_levels + ((state.count("Quest Point",self.player)//self.options.qp_per_level) * self.options.levels_per_qp)
                for method_name in relevent_methods:
                    loc = self.training_to_data[method_name]
                    method = self.training_to_row[method_name]
                    if "Unlock ~|Herblore|~ after Druidic Ritual" in loc.name:
                        return_list.extend([{"type":"text","text":f"{method.required_level} -> {method.required_level + 2} via "},{"type": "color", "color": "salmon", "text": loc.name},{"type":"text","text":"\n"}])
                        continue
                    return_list.extend([{"type":"text","text":f"{method.required_level} -> {method.required_level + delta_level} via "},{"type": "color", "color": "salmon", "text": loc.name},{"type":"text","text":"\n"}])
                return return_list
        elif dest_name.startswith("where "):
            _,location = dest_name.split(" ",2)
            if not location.startswith("chunk_"):
                return None
            _,id = location.split("_",2)
            if location not in self.region_code_to_name:
                location = f"{location}-1"
                if location not in self.region_code_to_name:
                    return None
            if not id.isnumeric():
                id,_ = id.split("-",2)
                if not id.isnumeric():
                    return None
            import webbrowser
            x = (int(id) // 256 ) * 64 + 32
            y = (int(id)  % 256 ) * 64 + 32
            webbrowser.open(f"https://explv.github.io/?centreX={str(x)}&centreY={str(y)}&centreZ=0&zoom=9",2)
            return [{"type":"text","text":f"Chunk {id} otherwise known as {self.region_code_to_name[location]}"}]
        else:
            return None

    def parse_rule(self, rule_element: RuleElement):
        if rule_element.type == "has": #literal ap item has
            return Has(rule_element.value)
        elif rule_element.type == "task":
            return Has(rule_element.value)
        elif rule_element.type == "chunk":
            return SafeCanReachRegion(rule_element.value)
        elif rule_element.type == "can_reach":
            return SafeCanReachRegion(rule_element.value)
        elif rule_element.type == "kill":
            return SafeCanReachRegion(rule_element.value)
        elif rule_element.type == "skill":
            skill,level = rule_element.value.rsplit("_",2)
            assert level.isdigit()
            if self.options.maximum_training_levels.get(skill,Options.MaxTrainingLevel.default) < int(level):
                return False_() #skill is outside of the maximum level
            if self.options.starting_skill_levels.get(skill,Options.StartingLevels.default) > int(level):
                return True_()
            if int(level) <= 1: return None
            if skill in ("Attack","Strength","Defence","Prayer","Hitpoints","Combat"):
                return And(SafeCanReachRegion("kill_Monster[+]"),Has("Quest Point",(int(level)-1)*2))
            if skill == "Slayer":
                return And(SafeCanReachRegion("PointSlayerMasters[+]"),Has("Quest Point",(int(level)-1)*2))
            if skill == "Ranged":
                return And(SafeCanReachRegion("kill_Monster[+]"),Has("Quest Point",(int(level)-1)*2),SafeCanReachRegion("Iron arrow"))
            return HasTraining(skill,int(level),self.options.qp_per_level.value,self.options.levels_per_qp.value)
        elif rule_element.type == "questPoints":
            return Has("Quest Point",int(rule_element.value))
        elif rule_element.type == "kudos":
            return Has("Kudo",int(rule_element.value))
        elif rule_element.type == "combatPoints":
            return Has("Combat Point",int(rule_element.value))
        elif rule_element.type.startswith("task_macro"):
            if rule_element.value not in task_macros:
                raise Exception("Task macro but it doesn't exist..."+rule_element.value)
            if rule_element.type.startswith("task_macrox"):
                _,count = rule_element.type.split("x",2)
                if count.isdigit():
                    count = int(count)
                    return HasFromList(*task_macros[rule_element.value],count=count)
            else:
                return HasAny(*task_macros[rule_element.value])
        else:
            #return None
            raise Exception("unknown rule fragment found "+rule_element.type)


    def generate_lambda(self, rule_list:list[RuleElement]):
        output_list = []
        if not rule_list:
            return None #if it's empty then let AP handle the default
        for rule in rule_list:
            temp_rule = self.parse_rule(rule)
            if temp_rule is not None: output_list.append(temp_rule)
        if len(output_list) > 1:
            return And(*output_list)
        elif len(output_list) == 1:
            return output_list[0]
        else:
            return None #if there's no valid rules, just let the default rule take over


    def create_regions(self) -> None:
        """
        called to place player's regions into the MultiWorld's regions list. If it's hard to separate, this can be done
        during generate_early or basic as well.
        """

        # First, create the "Menu" region to start
        menu_region = self.create_region("Menu")

        for region_row in region_rows:
            if region_row.id not in self.options.banned_chunks:
                self.create_region(region_row.id) #id is the name of the region, name is the name of the item that unlocks it

        for resource_row in resource_rows:
            self.create_region(resource_row.name)
        
        for monster_row in monster_drops:
            self.create_region(monster_row.name)

        # Removes the word "Area: " from the item name to get the region it applies to.
        # I figured tacking "Area: " at the beginning would make it _easier_ to tell apart. Turns out it made it worse
        # if area hasn't been set, then we shouldn't connect it
        if self.starting_area_item != "":
            starting_area_region = self.item_rows_by_name[self.starting_area_item].cannonical_chunk
            assert starting_area_region is not None
            starting_entrance = menu_region.create_exit(f"Start->{starting_area_region}")
            starting_entrance.access_rule = lambda state: state.has(self.starting_area_item, self.player)
            starting_entrance.connect(self.region_name_to_data[starting_area_region])


        for location in location_rows:
            self.create_location(location)
        for sub_location in sub_quests:
            self.create_location(sub_location)
        created_training_methods = []
        for training_method in training_methods:
            if self.create_training(training_method):
                created_training_methods.append(training_method)

        # place "Victory" at the option from the yaml

        goal_location_name = self.options.goal_location.value if self.options.goal_location.value in self.location_name_to_id else "~|Dragon Slayer I|~ Complete the quest"
        self.options.goal_location.value = goal_location_name
        real_goal_location = self.multiworld.get_location(goal_location_name, self.player)
        goal_location = OSRSMLocation(self.player,f"Victory {goal_location_name}",None,real_goal_location.parent_region)
        goal_location.place_locked_item(self.create_event("Victory"))
        real_goal_location.parent_region.locations.append(goal_location)

        #set_rules
        rr_entrances_cache:dict[str,tuple[Entrance,list]] = {}
        rr_entrances_cache_miss: list[str] = []

        for entrance in rr_entrances: #Region to Region connections
            if entrance.source in self.options.banned_chunks or entrance.dest in self.options.banned_chunks:
                continue
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_name = f"{sourceRegion.name} -> {destRegion.name}"
            if entrance_name in rr_entrances_cache:
                if entrance.rule:
                    temp_rule = self.generate_lambda(entrance.rule)
                    if temp_rule is not None: rr_entrances_cache[entrance_name][1].append(temp_rule)
                if entrance_name not in rr_entrances_cache_miss:
                    rr_entrances_cache_miss.append(entrance_name)
            else:
                temp_rule = self.generate_lambda(entrance.rule)
                if temp_rule is not None:
                    rr_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[temp_rule])
                else:
                    rr_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[])
        for entrance,rules in rr_entrances_cache.values():
            if len(rules) > 1:
                self.set_rule(entrance,Or(*rules))
            elif len(rules) == 1:
                self.set_rule(entrance,rules[0])
        
        re_entrances_cache:dict[str,tuple[Entrance,list]] = {}
        re_entrances_cache_miss: list[str] = []

        for entrance in re_entrances: #Region to rEsource connections
            if entrance.source in self.options.banned_chunks:
                continue
            if entrance.source == "Starting Items":
                if self.options.tutorial_island_items.value:
                    sourceRegion = self.region_name_to_data["Menu"]
                else:
                    continue
            else:
                sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_name = f"{sourceRegion.name} -> {destRegion.name}"
            if entrance_name in re_entrances_cache:
                if entrance.rule:
                    temp_rule = self.generate_lambda(entrance.rule)
                    if temp_rule is not None: re_entrances_cache[entrance_name][1].append(temp_rule)
                if entrance_name not in re_entrances_cache_miss:
                    re_entrances_cache_miss.append(entrance_name)
            else:
                temp_rule = self.generate_lambda(entrance.rule)
                if temp_rule is not None:
                    re_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[temp_rule])
                else:
                    re_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[])
        for entrance,rules in re_entrances_cache.values():
            if len(rules) > 1:
                self.set_rule(entrance,Or(*rules))
            elif len(rules) == 1:
                self.set_rule(entrance,rules[0])

        ee_entrances_cache:dict[str,tuple[Entrance,list]] = {}
        ee_entrances_cache_miss:list[str] = []

        for entrance in ee_entrances: #rEsource to rEsource connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_name = f"{sourceRegion.name} -> {destRegion.name}"
            if entrance_name in ee_entrances_cache:
                if entrance.rule:
                    temp_rule = self.generate_lambda(entrance.rule)
                    if temp_rule is not None: ee_entrances_cache[entrance_name][1].append(temp_rule)
                if entrance_name not in ee_entrances_cache_miss:
                    ee_entrances_cache_miss.append(entrance_name)
            else:
                temp_rule = self.generate_lambda(entrance.rule)
                if temp_rule is not None:
                    ee_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[temp_rule])
                else:
                    ee_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[])
        for entrance,rules in ee_entrances_cache.values():
            if len(rules) > 1:
                self.set_rule(entrance,Or(*rules))
            elif len(rules) == 1:
                self.set_rule(entrance,rules[0])

        me_entrances_cache:dict[str,tuple[Entrance,list]] = {}
        me_entrances_cache_miss:list[str] = []

        for entrance in me_entrances: #rEsource to rEsource connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_name = f"{sourceRegion.name} -> {destRegion.name}"
            if entrance_name in me_entrances_cache:
                if entrance.rule:
                    temp_rule = self.generate_lambda(entrance.rule)
                    if temp_rule is not None: me_entrances_cache[entrance_name][1].append(temp_rule)
                if entrance_name not in me_entrances_cache_miss:
                    me_entrances_cache_miss.append(entrance_name)
            else:
                temp_rule = self.generate_lambda(entrance.rule)
                if temp_rule is not None:
                    me_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[temp_rule])
                else:
                    me_entrances_cache[entrance_name] = (sourceRegion.connect(destRegion,entrance_name),[])
        for entrance,rules in me_entrances_cache.values():
            if len(rules) > 1:
                self.set_rule(entrance,Or(*rules))
            elif len(rules) == 1:
                self.set_rule(entrance,rules[0])

        for entrance in rm_entrances: #Region to Monster connections
            if entrance.source in self.options.banned_chunks:
                continue
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_obj = sourceRegion.connect(destRegion,None)
            rule = self.generate_lambda(entrance.rule)
            if rule is not None: self.set_rule(entrance_obj,rule)

        for entrance in mm_entrances: #Monster to Monster connections
            sourceRegion = self.region_name_to_data[entrance.source]
            destRegion = self.region_name_to_data[entrance.dest]
            entrance_obj = sourceRegion.connect(destRegion,None)
            rule = self.generate_lambda(entrance.rule)
            if rule is not None: self.set_rule(entrance_obj,rule)
        
        resolved_rate = self.options.max_drop_rate if self.options.full_drop_rate == 0 else self.options.full_drop_rate

        for monster in monster_drops:
            assert isinstance(monster, MonsterRow)
            for drop in monster.drops:
                if drop.rate > resolved_rate:
                    continue
                sourceRegion = self.region_name_to_data[monster.name]
                dest_name = drop.dest
                rule_list = None
                if drop.rule:
                    rule_list = self.generate_lambda(drop.rule)
                if "(noted)" in dest_name:
                    destRegion = self.region_name_to_data[drop.dest[:-8]]
                else:
                    destRegion = self.region_name_to_data[drop.dest]
                entrance_name = f"{sourceRegion.name} -> {dest_name}"
                entrance = sourceRegion.connect(destRegion,entrance_name,None)
                if rule_list is not None: self.set_rule(entrance,rule_list)

        for non_monster in non_monster_drops:
            assert isinstance(non_monster, MonsterRow)
            for drop in non_monster.drops:
                if drop.rate > resolved_rate:
                    continue
                sourceRegion = self.region_name_to_data[non_monster.name]
                dest_name = drop.dest
                rule_list = None
                if drop.rule:
                    rule_list = self.generate_lambda(drop.rule)
                if "(noted)" in dest_name:
                    destRegion = self.region_name_to_data[drop.dest[:-8]]
                else:
                    destRegion = self.region_name_to_data[drop.dest]
                entrance_name = f"{sourceRegion.name} -> {dest_name}"
                entrance = sourceRegion.connect(destRegion,entrance_name,None)
                if rule_list is not None: self.set_rule(entrance,rule_list)

        for location_row in location_rows:
            if location_row.name in self.pre_completed_locations or location_row.name in self.options.exclude_locations:
                continue
            if location_row.parent_region in self.options.banned_chunks:
                continue
            if location_row.rule:
                location = self.multiworld.get_location(location_row.name,self.player)
                fake_location = self.multiworld.get_location(location_row.name+" event",self.player)
                rule = self.generate_lambda(location_row.rule)
                if rule is not None:
                    if not (location_row.name in self.pre_completed_locations or location_row.name in self.options.exclude_locations):
                        self.set_rule(location,rule)
                    if location_row.name == goal_location_name:
                        self.set_rule(goal_location,rule)
                    self.set_rule(fake_location,rule)
                if location_row.quest_point_reward > 0:
                    qp_loc = self.multiworld.get_location("Points: " + location_row.name,self.player)
                    if rule is not None:
                        self.set_rule(qp_loc,rule)
                if location_row.combat_point_reward > 0:
                    qp_loc = self.multiworld.get_location("CombatPoints: " + location_row.name,self.player)
                    if rule is not None:
                        self.set_rule(qp_loc,rule)
                if location_row.kudos_reward > 0:
                    qp_loc = self.multiworld.get_location("Kudos: " + location_row.name,self.player)
                    if rule is not None:
                        self.set_rule(qp_loc,rule)
        for location_row in sub_quests:
            if location_row.name in self.pre_completed_locations or location_row.name in self.options.exclude_locations:
                continue
            if location_row.parent_region in self.options.banned_chunks:
                continue
            if location_row.rule:
                location = self.multiworld.get_location(location_row.name,self.player)
                rule = self.generate_lambda(location_row.rule)
                if rule is not None: #subquests can't be excluded or precompleted as they aren't real
                    self.set_rule(location,rule)
                if location_row.quest_point_reward > 0:
                    raise Exception("This shouldn't happen but i want to know if it does "+location_row.name)
                if location_row.combat_point_reward > 0:
                    qp_loc = self.multiworld.get_location("CombatPoints: " + location_row.name,self.player)
                    if rule is not None:
                        self.set_rule(qp_loc,rule)
                if location_row.kudos_reward > 0:
                    raise Exception("This shouldn't happen but i want to know if it does "+location_row.name)
        for training_method in created_training_methods:
            if training_method.rule:
                method = self.get_location(f"Training {training_method.skill_name}: {training_method.task_name}")
                rule = self.generate_lambda(training_method.rule)
                if rule is not None:
                    self.set_rule(method,rule)

        self.multiworld.completion_condition[self.player] = lambda state: (state.has("Victory", self.player))
        #create_items
        itempool:list[Item]= []
        for item_row in item_rows:
            if item_row.name not in [self.starting_area_item]:
                for c in range(item_row.amount):
                    item = self.create_item(item_row.name)
                    itempool.append(item)

        
        #culling time

        base_state = CollectionState(self.multiworld)
        for item in itempool:
            base_state.collect(item, True)
        temp_state = base_state.copy()


        temp_state.sweep_for_advancements()
        if not self.multiworld.completion_condition[self.player](temp_state):
            max_trained_levels:dict[str, int] = {}
            for item in temp_state.prog_items[self.player].keys():
                if item.startswith("Training_"):
                    _,skill,level = item.split("_",3)
                    if skill in max_trained_levels:
                        max_trained_levels[skill] = max(max_trained_levels[skill],int(level))
                    else:
                        max_trained_levels[skill] = int(level)
            logger.error(max_trained_levels)
            raise OptionError("Game isn't beatable with current settings")

        if not self.options.disable_chunk_culling:
            region_loc_count_lookup = {
                region: len([loc for loc in region.locations if loc.address]) for region in self.get_regions()
            }

            pre_placed_advancements = [loc for loc in self.get_locations() if loc.advancement]
                

            all_state = base_state.copy()
            all_state.sweep_for_advancements(locations=pre_placed_advancements)
            if all_state.stale[self.player]:
                all_state.update_reachable_regions(self.player)
            max_chance = sum([region_loc_count_lookup[region] for region in all_state.reachable_regions[self.player]]) - len(itempool)
            base_itempool = itempool.copy()
            self.random.shuffle(base_itempool)
            exit_counter = 0
            for i in range(20):
                short_pool = base_itempool[i::20]
                temp_state = base_state.copy()
                for item in short_pool:
                    temp_state.remove(item)
                temp_state.sweep_for_advancements(locations=pre_placed_advancements)
                if self.multiworld.completion_condition[self.player](temp_state):
                    if temp_state.stale[self.player]:
                        temp_state.update_reachable_regions(self.player)
                    curr_chance = sum([region_loc_count_lookup[region] for region in temp_state.reachable_regions[self.player]]) - len(itempool)
                    for item in short_pool:
                        rand_value = 0 if curr_chance < 0 else self.random.randint(0,max_chance)
                        if rand_value<curr_chance:
                            rand_value = 0 if curr_chance < 0 else self.random.randint(0,max_chance) #Roll the dice again, if we pass this time just demote to useful
                            base_state.remove(item) #Either it's being removed from the item pool or converted to Useful
                            if rand_value<curr_chance:
                                itempool.remove(item)
                            else: #This way an item that had a low chance to get removed that got unlucky will probally stay, but dice be dice :)
                                item.classification = ItemClassification.useful
                        if rand_value == 0:
                            exit_counter += 1
                            if exit_counter > 5:
                                break
                    if exit_counter > 5:
                        break

        self.multiworld.itempool+=itempool
        self.items_already_created = len(itempool)
        all_state = CollectionState(self.multiworld)
        for item in itempool:
            all_state.collect(item,True)
        all_state.sweep_for_advancements()

        reachable_loc_map:dict[Location,int] = {}
        region_depth_cache:dict[str,int]= {}
        max_depth = 0

        #now remove regions/locations that aren't reachable with the reduced itempool
        regions = self.multiworld.regions.region_cache[self.player]
        temp_regions = regions.copy()
        for region_name, region in temp_regions.items():
            if all_state.can_reach_region(region_name,self.player):
                depth = 0
                if region.name != self.origin_region_name:
                    if region.name in region_depth_cache:
                        depth = region_depth_cache[region.name]
                    else:
                        temp_path = all_state.path[region]
                        while temp_path[1] is not None:
                            temp_path = temp_path[1]
                            depth += 1
                        region_depth_cache[region.name] = depth
                max_depth = max(max_depth,depth)
                temp_locs = region.locations.copy()
                for loc in temp_locs:
                    if not all_state.can_reach_location(loc.name,self.player):
                        region.locations.remove(loc)
                    else:
                        if loc.address: reachable_loc_map[loc] = depth
            else:
                for entrance in region.entrances: #disconnect entrances
                    if entrance.parent_region:
                        entrance.parent_region.exits.remove(entrance)
                for exit in region.exits: #disconnect exists
                    if exit.connected_region:
                        exit.connected_region.entrances.remove(exit)
                for location in region.locations: #delete all the locations in that region
                    del self.multiworld.regions.location_cache[self.player][location.name]
                del regions[region_name] #delete the region

        if not self.options.disable_task_culling.value:
            location_list = list(reachable_loc_map.keys())
            #get my fraction parts
            maximum_locations = len(location_list)
            items_created = self.items_already_created
            locations_created = len(location_list)
            #start to cull
            self.random.shuffle(location_list) #look at them in random order, just to make sure it's not going to cull from whoever was made first
            for loc in location_list:
                depth = min(reachable_loc_map[loc],max_depth)
                goal_number = (locations_created - items_created)  #(current locs - locs needed) ~= locs needed to be removed * current depth
                if depth == 0:
                    continue #goal number check covered by breaking early
                if (
                        (self.random.randint(0,maximum_locations) < goal_number)+
                        (self.random.randint(0,maximum_locations) < goal_number)+
                        (self.random.randint(0,max_depth) < depth)+
                        (self.random.randint(0,max_depth) < depth)
                    ) >= 1:
                    assert loc.parent_region
                    loc.parent_region.locations.remove(loc)
                    locations_created -= 1
                    #logger.info(f"Location {loc.name} deleted, {rolled_value}/{goal_number}/{maximum_locations}, {locations_created - items_created} left")
                    if not self.multiworld.completion_condition[self.player](all_state):
                        logger.error(f"HOW DID {loc.name} BREAK THIS???")
                        raise Exception("Somehow location culling removed a load bearing location, this should never have happened")
                    if locations_created <= items_created:
                        break #Exit early if we've already removed enough
            logger.error(f"Deleted {maximum_locations-locations_created} filler from {self.player_name}, {locations_created - items_created} remains")

        #visualize_regions(self.region_name_to_data["chunk_11937"],"osrs_regions.puml",show_locations=False,show_entrance_names=False,show_other_regions=False)

    def create_items(self) -> None:
        itempool = []

        un_filled_loc_size = len(self.multiworld.get_unfilled_locations(self.player)) - self.items_already_created
        while len(itempool) < un_filled_loc_size:
            itempool.append(self.create_filler())
        

        self.multiworld.itempool += itempool

    def get_filler_item_name(self) -> str:
        return "Area: Nothing :("

    def create_location(self, location_row:LocationRow):
        if location_row.name in self.pre_completed_locations:
            #Don't do most of this, just add the events to precollected :)
            self.push_precollected(self.create_event(location_row.name))
            if location_row.quest_point_reward>0:
                self.push_precollected(self.create_quest_point_event(location_row))
            if location_row.kudos_reward>0:
                self.push_precollected(self.create_kudos_event(location_row))
            if location_row.combat_point_reward > 0:
                self.push_precollected(self.create_combat_points_event(location_row))
            return
        if location_row.parent_region in self.options.banned_chunks:
            return
        if location_row.category == "goal" or location_row.category == "subquest" or location_row.category == "event":
            location_id = None
        elif location_row.name not in self.location_name_to_id:
            print(location_row.name)
            breakpoint()
            exit()
        else:
            location_id = self.location_name_to_id[location_row.name]
        if location_row.name in self.options.exclude_locations:
            return #don't do ANY of this

        location = OSRSMLocation(self.player,location_row.name,location_id)
        self.location_name_to_data[location_row.name] = location

        region = self.region_name_to_data["Menu"]
        if location_row.parent_region:
            region = self.region_name_to_data[location_row.parent_region]
        location.parent_region = region
        region.locations.append(location)

        if location_row.category == "subquest" or location_row.category == "event":
            location.show_in_spoiler = False
            location.place_locked_item(self.create_event(location_row.name))
        else:
            fake_location = OSRSMLocation(self.player,location_row.name+" event",None)
            fake_location.show_in_spoiler = False
            fake_location.parent_region = region
            fake_location.place_locked_item(self.create_event(location_row.name))
            region.locations.append(fake_location)
        if location_row.quest_point_reward > 0:
            qp_name = "Points: " + location_row.name
            qp_loc = OSRSMLocation(self.player,qp_name,None)
            qp_loc.show_in_spoiler = False
            self.location_name_to_data[qp_name] = qp_loc
            qp_loc.parent_region = region
            qp_loc.place_locked_item(self.create_quest_point_event(location_row))
            region.locations.append(qp_loc)
        if location_row.kudos_reward > 0:
            qp_name = "Kudos: " + location_row.name
            qp_loc = OSRSMLocation(self.player,qp_name,None)
            qp_loc.show_in_spoiler = False
            self.location_name_to_data[qp_name] = qp_loc
            qp_loc.parent_region = region
            qp_loc.place_locked_item(self.create_kudos_event(location_row))
            region.locations.append(qp_loc)
        if location_row.combat_point_reward > 0:
            qp_name = "CombatPoints: " + location_row.name
            qp_loc = OSRSMLocation(self.player,qp_name,None)
            qp_loc.show_in_spoiler = False
            self.location_name_to_data[qp_name] = qp_loc
            qp_loc.parent_region = region
            qp_loc.place_locked_item(self.create_combat_points_event(location_row))
            region.locations.append(qp_loc)
    
    def create_training(self, training_row:TrainingRow) -> bool:
        if training_row.parent_region in self.options.banned_chunks:
            return False
        parent_region = self.get_region(training_row.parent_region)

        if training_row.task_name == "Unlock ~|Herblore|~ after Druidic Ritual":  # We don't want to be herblore 10 etc after druidic ritual
            training_level = training_row.required_level + 3
        else:
            training_level = training_row.required_level + self.options.base_training_levels.value
        if training_level > 99:
            # self.options.base_training_levels can push the required level over 99, making the training irrelevant.
            return False

        method = OSRSMLocation(self.player,f"Training {training_row.skill_name}: {training_row.task_name}",None,parent_region)
        method.place_locked_item(self.create_training_event(training_row.skill_name, training_level))
        method.show_in_spoiler = False
        parent_region.locations.append(method)
        self.training_to_data[method.name] = method
        self.training_to_row[method.name] = training_row
        return True

    def create_region(self, name: str) -> "Region":
        region = Region(name, self.player, self.multiworld)
        self.region_name_to_data[name] = region
        self.multiworld.regions.append(region)
        return region

    def create_item(self, name: str) -> "Item":
        if name in self.item_rows_by_name:
            item = self.item_rows_by_name[name]
            item_id = None
            if name in self.item_name_to_id:
                item_id = self.item_name_to_id[name]
            return OSRSMItem(item.name, item.progression, item_id, self.player)
        raise Exception("Not able to find item "+name)

    def create_event(self, event: str):
        # while we are at it, we can also add a helper to create events
        return OSRSMItem(event, ItemClassification.progression, None, self.player)

    def create_training_event(self, skill_name: str, skill_level: int):
        return OSRSMTrainingItem(skill_name, skill_level, self.player)

    def create_quest_point_event(self, location_row: LocationRow):
        return OSRSMQuestPointItem(location_row.quest_point_reward, location_row.name, self.player)

    def create_kudos_event(self, location_row: LocationRow):
        return OSRSMKudosItem(location_row.kudos_reward, location_row.name, self.player)

    def create_combat_points_event(self, location_row: LocationRow):
        return OSRSMCombatPointsItem(location_row.combat_point_reward, location_row.name, self.player)

    def collect(self, state: CollectionState, item: Item) -> bool:
        if item.code is not None:
            return super().collect(state,item)
        # Asserts help type checking, but keep performance on frozen AP (`-O` command line argument), because
        # isinstance is slow, and asserts cease to exist with `-O`.
        assert isinstance(item, OSRSMItem)
        item_type = item.item_type
        if item_type == "quest_point":
            assert isinstance(item, OSRSMQuestPointItem)
            qp_count = item.quest_point_reward
            state.add_item(item="Quest Point",player=self.player,count=qp_count)
        elif item_type == "combat_points":
            assert isinstance(item, OSRSMCombatPointsItem)
            combat_point_reward = item.combat_point_reward
            state.add_item(item="Combat Point", player=self.player, count=combat_point_reward)
        elif item_type == "kudos":
            assert isinstance(item, OSRSMKudosItem)
            kudos = item.kudos_reward
            state.add_item(item="Kudo",player=self.player,count=kudos)
        elif item_type == "training":
            # Assert to help type checking, but keep performance on frozen AP or `-O` command line argument.
            assert isinstance(item, OSRSMTrainingItem)
            skill_level = item.skill_level
            # Check the current Max Training level for this skill, and increase it if `skill_level` is higher.
            psuedo_item_name = item.pseudo_item_name
            current_max_level = state.prog_items[self.player][psuedo_item_name]
            if skill_level > current_max_level:
                state.prog_items[self.player][psuedo_item_name] = skill_level
        return super().collect(state, item)
    
    def remove(self, state: CollectionState, item: Item) -> bool:
        if item.code is not None:
            return super().remove(state,item)
        # Asserts help type checking, but keep performance on frozen AP (`-O` command line argument), because
        # isinstance is slow, and asserts cease to exist with `-O`.
        assert isinstance(item, OSRSMItem)
        item_type = item.item_type
        if item_type == "quest_point":
            assert isinstance(item, OSRSMQuestPointItem)
            qp_count = item.quest_point_reward
            state.remove_item(item="Quest Point",player=self.player,count=qp_count)
        elif item_type == "combat_points":
            assert isinstance(item, OSRSMCombatPointsItem)
            combat_point_reward = item.combat_point_reward
            state.remove_item(item="Combat Point",player=self.player,count=combat_point_reward)
        elif item_type == "kudos":
            assert isinstance(item, OSRSMKudosItem)
            kudos = item.kudos_reward
            state.remove_item(item="Kudo",player=self.player,count=kudos)
        elif item_type == "training":
            if state.count(item.name, self.player) == 1:
                # The last Training event for this level is being removed, so the Max Training psuedo-item may need to
                # be updated.
                # Assert to help type checking, but keep performance on frozen AP or `-O` command line argument.
                assert isinstance(item, OSRSMTrainingItem)
                skill_level = item.skill_level
                skill_name = item.skill_name
                # Check the current Max Training level for this skill, and decrease it if it is equal to `skill_level`.
                psuedo_item_name = item.pseudo_item_name
                current_max_level = state.prog_items[self.player][psuedo_item_name]
                if current_max_level == skill_level:
                    # Find the next highest training level for this skill in the state.
                    next_highest_level = 0
                    for i in reversed(range(1, skill_level)):
                        event_item_name = f"Training_{skill_name}_{i}"
                        if state.has(event_item_name, self.player):
                            next_highest_level = i
                            break
                    state.prog_items[self.player][psuedo_item_name] = next_highest_level
        return super().remove(state, item)


@dataclasses.dataclass()
class SafeCanReachRegion(CanReachRegion["OSRSMWorld"],game="OSRSMWorld"):

    class Resolved(CanReachRegion.Resolved):
        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            return self.region_name in state.multiworld.regions.region_cache[self.player] and state.can_reach_region(self.region_name, self.player)


@dataclasses.dataclass()
class HasTraining(Rule["OSRSMWorld"],game="OSRSMWorld"):
    skill_name: str
    skill_level: int
    qp_run: int
    qp_rise: int
    def _instantiate(self, world: "OSRSMWorld") -> Rule.Resolved:
        if self.skill_name in world.options.starting_skill_levels and self.skill_level <= world.options.starting_skill_levels[self.skill_name]:
            return True_.Resolved(player=world.player)
        if self.skill_name in world.options.maximum_training_levels and self.skill_level > world.options.maximum_training_levels[self.skill_name]:
            return False_.Resolved(player=world.player)
        pseudo_item_name = f"_Max_Training_{self.skill_name}"
        return self.Resolved(self.skill_name,self.skill_level,self.qp_run,self.qp_rise,pseudo_item_name,player=world.player)

    class Resolved(Rule.Resolved):
        skill_name: str
        skill_level: int
        qp_run: int
        qp_rise: int
        _max_training_psuedo_item_name: str
        skip_cache=True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # Check for training of self.skill_level and higher.
            max_training_level = state.count(self._max_training_psuedo_item_name, self.player)
            if max_training_level >= self.skill_level:
                return True
            # Check for training from lower levels than self.skill_level, accounting for qp_rise.
            allowed_lower_training_level = max(1,self.skill_level-self.qp_rise*(state.count("Quest Point",self.player)//self.qp_run))
            return max_training_level >= allowed_lower_training_level

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {f"Training_{self.skill_name}":{id(self)},"Quest Point":{id(self)}}
        
        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            result = self._evaluate(state)
            if result:
                return f"Can train level {self.skill_level} {self.skill_name}"
            else:
                training_levels = sorted([int(v.rsplit("_",1)[1]) for v in state.prog_items[self.player] if v.startswith(f"Training_{self.skill_name}")])
                training_level = training_levels[-1] if len(training_levels)>0 else 0
                quest_training = self.qp_rise*(state.count("Quest Point",self.player)//self.qp_run)
                return f"Can't train level {self.skill_level} {self.skill_name} ({f'{training_level+quest_training}' if training_level else 'None'})"
        
        @override
        def explain_json(self, state: CollectionState|None = None) ->list[JSONMessagePart]:
            return [{"type":"text","text":self.explain_str(state)}]
        
        def __str__(self) -> str:
            return f"Train level {self.skill_level} {self.skill_name}"

