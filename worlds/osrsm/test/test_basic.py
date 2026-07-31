from . import OSRSMTestBase
from rule_builder import *
from .. import *
import unittest
from ..Options import MaxDropRate, FullMaxDropRate, DisableChunkCulling, GoalType
from ..LogicCSV.regions_generated2 import region_rows, resource_rows 
from ..LogicCSV.locations_generated2 import location_rows, sub_quests
from ..LogicCSV.monsters_generated2 import monster_drops
from ..LogicCSV.macros_generated2 import skill_names

def get_logical_path(state: CollectionState, target: Region) -> None:
    from BaseClasses import Region
    from typing import Tuple, Iterator,Union
    from itertools import zip_longest

    def flist_to_iter(path_value) -> Iterator[str]:
        while path_value:
            region_or_entrance, path_value = path_value
            yield region_or_entrance

    def get_path(state: CollectionState, region: Region) -> list[Union[Tuple[str, str], Tuple[str, None]]]:
        reversed_path_as_flist = state.path.get(region, (str(region), None))
        string_path_flat = reversed(list(map(str, flist_to_iter(reversed_path_as_flist))))
        # Now we combine the flat string list into (region, exit) pairs
        pathsiter = iter(string_path_flat)
        pathpairs = zip_longest(pathsiter, pathsiter)
        return list(pathpairs)

    paths = get_path(state=state, region=target)
    for k, v in paths:
        if v:
            print(v)

class BingoTests(OSRSMTestBase):
    options = {
        "goal_type": GoalType.option_bingo
    }

class AgilityTests(OSRSMTestBase):
    options = {
        "max_drop_rate": MaxDropRate.range_end,
        "full_drop_rate": FullMaxDropRate.range_end,
        "disable_chunk_culling": DisableChunkCulling.option_disabled,
        "disable_task_culling": True,
        "maximum_training_levels": {skill_name:((99 if skill_name != "Agility" else 70) if skill_name != "Combat" else 100) for skill_name in skill_names}
    }

    def test_seventy_two_agility_not_created(self)->None:
        self.assertNotIn("Access the Wilderness Chaos Temple stepping stone ~|shortcut|~",self.multiworld.regions.location_cache[self.player].keys())

class ThievingTests(OSRSMTestBase):
    options = {
        "max_drop_rate": MaxDropRate.range_end,
        "full_drop_rate": FullMaxDropRate.range_end,
        "disable_chunk_culling": DisableChunkCulling.option_disabled,
        "disable_task_culling": True,
        "maximum_training_levels": {skill_name:((99 if skill_name != "Thieving" else 70) if skill_name != "Combat" else 100) for skill_name in skill_names}
    }

    def test_seventy_two_thieving_not_created(self)->None:
        self.assertNotIn("Armour Case: ~|Elite black platelegs|~",self.multiworld.regions.location_cache[self.player].keys())

class FarmingTests(OSRSMTestBase):
    options = {
        "max_drop_rate": MaxDropRate.range_end,
        "full_drop_rate": FullMaxDropRate.range_end,
        "disable_chunk_culling": DisableChunkCulling.option_disabled,
        "disable_task_culling": True,
        "maximum_training_levels": {skill_name:((99 if skill_name != "Farming" else 70) if skill_name != "Combat" else 100) for skill_name in skill_names}
    }

    def test_eighty_three_not_created(self)->None:
        self.assertNotIn("Grow a ~|spirit tree|~",self.multiworld.regions.location_cache[self.player].keys())

class LowDropRateTests(OSRSMTestBase):
    options = {
        "max_drop_rate": 128,
        "full_drop_rate": 128,
        "disable_chunk_culling": DisableChunkCulling.option_disabled,
        "disable_task_culling": True
    }

    def test_dark_totem_not_created(self)->None:
        self.assertNotIn("Make a dark totem",self.multiworld.regions.location_cache[self.player].keys())

class FullTests(OSRSMTestBase):
    options = {
        "max_drop_rate": MaxDropRate.range_end,
        "full_drop_rate": FullMaxDropRate.range_end,
        "disable_chunk_culling": DisableChunkCulling.option_disabled,
        "disable_task_culling": True
    }

    def test_creates_all_regions(self)->None:
        all_state = self.multiworld.get_all_state()
        region_cache = self.multiworld.regions.region_cache[1]
        for region_row in region_rows:
            assert isinstance(region_row,RegionRow)
            with self.subTest(region_name=region_row.id):
                self.assertIn(region_row.id,region_cache,f"Region {region_row.id} was not created")
                self.assertTrue(all_state.can_reach_region(region_row.id,1),f"Cannot reach region {region_row.id}")
    
    def test_creates_all_resources(self)->None:
        all_state = self.multiworld.get_all_state()
        region_cache = self.multiworld.regions.region_cache[1]
        for region_row in resource_rows:
            assert isinstance(region_row,ResourceRow)
            with self.subTest(region_name=region_row.name):
                self.assertIn(region_row.name,region_cache,f"Resource {region_row.name} was not created")
                self.assertTrue(all_state.can_reach_region(region_row.name,1),f"Cannot reach resource {region_row.name}")
    
    def test_creates_all_monsters(self)->None:
        all_state = self.multiworld.get_all_state()
        region_cache = self.multiworld.regions.region_cache[1]
        for region_row in monster_drops:
            assert isinstance(region_row,MonsterRow)
            with self.subTest(region_name=region_row.name):
                self.assertIn(region_row.name,region_cache,f"Drop table {region_row.name} was not created")
                self.assertTrue(all_state.can_reach_region(region_row.name,1),f"Cannot reach drop table {region_row.name}")
    
    def test_creates_all_sub_quests(self)->None:
        all_state = self.multiworld.get_all_state()
        location_cache = self.multiworld.regions.location_cache[1]
        for sub_quest in sub_quests:
            assert isinstance(sub_quest,LocationRow)
            with self.subTest(sub_quest_name=sub_quest.name):
                self.assertIn(sub_quest.name,location_cache,f"Sub Quest step {sub_quest.name} was not created")
                self.assertTrue(all_state.can_reach_location(sub_quest.name,1),f"Sub Quest step {sub_quest.name} is not reachable")

    def test_creates_all_locations(self)->None:
        all_state = self.multiworld.get_all_state()
        location_cache = self.multiworld.regions.location_cache[1]
        for location_row in location_rows:
            assert isinstance(location_row,LocationRow)
            if location_row.category == "bingo":
                continue #skip bingo locations
            with self.subTest(location_name=location_row.name):
                self.assertIn(location_row.name,location_cache,f"Location {location_row.name} was not created")
                self.assertTrue(all_state.can_reach_location(location_row.name,1),f"Location {location_row.name} is not reachable")

    def test_camdozaal_not_sphere_one(self) -> None:
        self.assertFalse( self.can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~"))
        self.assertTrue(self.multiworld.get_all_state().can_reach_location("(Camdozaal) Obtain a ~|barronite handle|~",self.player))

    def test_ardougne_cloak_not_sphere_one(self) -> None:
        self.assertFalse( self.can_reach_location("~|Ardougne Diary#Easy|~ Complete the Easy Diary"))
        self.assertTrue(self.multiworld.get_all_state().can_reach_location("~|Ardougne Diary#Easy|~ Complete the Easy Diary",self.player))

    def test_should_be_able_to_train_smithing(self) -> None:
        self.collect_by_name("Area: Lumbridge Castle")
        self.assertFalse( self.can_reach_location("Smith a ~|bronze mace|~"))
        self.collect_by_name("Area: East Lumbridge Swamp")
        self.assertTrue(  self.can_reach_location("Smith a ~|bronze mace|~"))

    def test_weapon_poison_not_sphere_one(self)-> None:
        self.assertFalse(self.can_reach_region("Weapon poison(+)"))
    
    def test_can_reach_max_quest_levels(self)-> None:
        all_state = self.multiworld.get_all_state()
        def assert_min_training(self:OSRSMTestBase,state:CollectionState,skill_name:str,min_level:int):
            from .. import HasTraining
            world:OSRSMWorld = self.multiworld.worlds[self.player]
            rule = world.parse_rule(RuleElement("skill",f"{skill_name}_{str(min_level)}"))
            if rule is not None:
                self.assertTrue(rule.resolve(world)(state))
        assert_min_training(self,all_state,"Attack",50)
        assert_min_training(self,all_state,"Strength",60)
        assert_min_training(self,all_state,"Defence",65)
        assert_min_training(self,all_state,"Ranged",62)
        assert_min_training(self,all_state,"Prayer",50)
        assert_min_training(self,all_state,"Magic",75)
        assert_min_training(self,all_state,"Runecraft",60)
        assert_min_training(self,all_state,"Construction",70)
        assert_min_training(self,all_state,"Agility",70)
        assert_min_training(self,all_state,"Herblore",70)
        assert_min_training(self,all_state,"Thieving",72)
        assert_min_training(self,all_state,"Crafting",70)
        assert_min_training(self,all_state,"Fletching",60)
        assert_min_training(self,all_state,"Slayer",69)
        assert_min_training(self,all_state,"Hunter",70)
        assert_min_training(self,all_state,"Mining",72)
        assert_min_training(self,all_state,"Smithing",70)
        assert_min_training(self,all_state,"Fishing",62)
        assert_min_training(self,all_state,"Cooking",70)
        assert_min_training(self,all_state,"Firemaking",75)
        assert_min_training(self,all_state,"Woodcutting",71)
        assert_min_training(self,all_state,"Farming",70)
    
    def test_can_reach_max_levels(self)-> None:
        all_state = self.multiworld.get_all_state()
        world = self.multiworld.worlds[1]
        def assert_min_training(self:OSRSMTestBase,state:CollectionState,skill_name:str,min_level:int):
            world:OSRSMWorld = self.multiworld.worlds[self.player]
            rule = world.parse_rule(RuleElement("skill",f"{skill_name}_{str(min_level)}"))
            if rule is not None:
                self.assertTrue(rule.resolve(world)(state))
        for skill in skill_names:
            with self.subTest(skill_name=skill):
                assert_min_training(self,all_state,skill,99)

    def test_state_doodles(self) -> None:
        all_state = self.multiworld.get_all_state()
        all_state.sweep_for_advancements()
        world:OSRSMWorld = self.multiworld.worlds[self.player]
        rule_a = Has('~|Plague City|~ 1')
        rule_b = CanReachRegion('Dwellberries')
        rule_c = CanReachRegion('Alrena')
        rule_d = Has('Area: Chaos Druid Tower')
        rule_e = Has('~|Rune Mysteries|~ 1')
        rule1 = And(rule_a,rule_b)
        rule2 = And(rule_b,rule_c)
        rule3 = And(rule_a,rule_d)
        rule4 = And(rule_a,rule_c)
        rule5 = And(rule_b,rule_d)
        rule6 = And(rule_c,rule_d)
        rule7 = And(rule_e, rule_b)
        rule0 = Or(rule_a,rule_b)
        self.assertTrue(rule_a.resolve(world)(all_state)) #passes
        self.assertTrue(rule_b.resolve(world)(all_state)) #passes
        self.assertTrue(rule_c.resolve(world)(all_state)) #passes
        self.assertTrue(rule_d.resolve(world)(all_state)) #passes
        self.assertTrue(rule_e.resolve(world)(all_state)) #passes
        self.assertTrue( rule0.resolve(world)(all_state)) #passes
        self.assertTrue( rule2.resolve(world)(all_state)) #passes
        self.assertTrue( rule3.resolve(world)(all_state)) #passes
        self.assertTrue( rule4.resolve(world)(all_state)) #passes
        self.assertTrue( rule5.resolve(world)(all_state)) #passes
        self.assertTrue( rule6.resolve(world)(all_state)) #passes
        self.assertTrue( rule7.resolve(world)(all_state)) #passes
        self.assertTrue( rule1.resolve(world)(all_state))  #fails
            
    def test_lumbridge_diary_not_in_logic(self)-> None:
        assert isinstance(self.world,OSRSMWorld)
        self.assertEqual(self.multiworld.get_all_state().prog_items[self.player]["Quest Point"], int(self.world.location_name_to_row["Buy the ~|Quest point cape|~"].rule[0].value))
        self.assertTrue(self.multiworld.get_all_state().can_reach_location("~|Lumbridge and Draynor Diary#Elite|~ Task 6",self.player))

    def test_items_needed_for_task(self)-> None:
        test_suite = {
            "Kill ~|Zulrah|~":["Area: Underground Pass Entrance"],
            "~|Fairytale I - Growing Pains|~ Complete the quest": ["Area: Nature Grotto"],
            "Wield a ~|dorgeshuun crossbow|~":["Area: Wizards\' Tower"],
            "~|Troll Stronghold|~ Complete the quest":["Area: Troll Stronghold"],
            "Kill ~|Callisto|~":["Area: Demonic Ruins"],
            "Complete ~|Keldagrim tasks|~ for Mining xp":["Area: Rellekka Peninsula"],
            "~|Morytania Diary#Medium|~ Task 8":["Area: West Lumbridge Swamp"]
        }
        for goal,item_list in test_suite.items():
            with self.subTest(goal=goal,item_list=item_list):
                all_state = self.multiworld.get_all_state(perform_sweep=False)
                for item in item_list:
                    all_state.remove_item(item,self.player,1)
                all_state.sweep_for_advancements()
                loc = self.multiworld.get_location(goal,self.player)
                self.assertFalse(loc.can_reach(all_state))
                new_all_state = self.multiworld.get_all_state()
                self.assertTrue(loc.can_reach(new_all_state))
