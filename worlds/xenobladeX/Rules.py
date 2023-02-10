from functools import partial
from typing import Callable, Dict
from BaseClasses import CollectionState, MultiWorld
from .Locations import create_location_event
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

def set_rules(world: MultiWorld, player: int):
    """Setting all the rules for region connections and region->item connections"""
    victory_item = create_item_event(world, "Victory", player)
    final_boss_location = create_location_event(world, "Menu", "EBK: Lao", player)
    final_boss_location.access_rule = lambda state: True
    final_boss_location.place_locked_item(victory_item)
    finish: Callable[[CollectionState], bool] = lambda state: state.has("Victory", player)
    # world.completion_condition[player] = finish

    for region in world.regions:
        requirements:list[Req] = []
        for subregion in region.name.split("+"):
            requirements.extend(_get_requirements_by_subregion(subregion))
        connect_regions(world, player, "Menu", region.name, partial(
            has_items, player=player, requirements=requirements))
