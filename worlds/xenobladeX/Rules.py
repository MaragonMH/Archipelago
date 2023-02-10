from functools import partial
from BaseClasses import MultiWorld
from .Regions import connect_regions
from .Items import has_items, create_item_event
from .dataType import Rule, Requirement as Req
from .regions.key import doll_regions, fnet_regions
from .regions.chapters import chapter_regions
from .regions.friends import friends_nagi_regions, friends_l_regions, friends_lao_regions, friends_gwin_regions, friends_frye_regions, \
    friends_doug_regions, friends_phog_regions, friends_elma_regions, friends_lin_regions, friends_celica_regions, \
    friends_irina_regions, friends_murderess_regions, friends_hope_regions, friends_mia_regions
from .regions.fieldSkills import mechanical_regions, biological_regions, archeological_regions

# Requirements to reach this region
xenobladeXRegionRules: list[list[Rule]] = [
    chapter_regions,
    friends_nagi_regions,
    friends_l_regions,
    friends_lao_regions,
    friends_gwin_regions,
    friends_frye_regions,
    friends_doug_regions,
    friends_phog_regions,
    friends_elma_regions,
    friends_lin_regions,
    friends_celica_regions,
    friends_irina_regions,
    friends_murderess_regions,
    friends_hope_regions,
    friends_mia_regions,
    doll_regions,
    fnet_regions,
    mechanical_regions,
    biological_regions,
    archeological_regions,
]

def _get_requirements_by_subregion(subregion:str) -> list[Req]:
    for data_regions in xenobladeXRegionRules:
        requirements:list[Req] = []
        for rule in data_regions:
            requirements.extend(rule.requirements)
            if rule.region == subregion:
                return requirements
    return []

def set_rules(world: MultiWorld, player: int, item_name_to_id):
    """Setting all the rules for region connections and region->item connections"""
    world.get_location("EBK: Lao", player).place_locked_item(
        create_item_event("KEY: Victory", player, item_name_to_id["KEY: Victory"]))
    world.completion_condition[player] = lambda state: state.has("KEY: Victory", player)

    for region in world.regions:
        requirements:list[Req] = []
        for subregion in region.name.split("+"):
            requirements.extend(_get_requirements_by_subregion(subregion))
        connect_regions(world, player, "Menu", region.name, partial(
            has_items, player=player, requirements=requirements))
