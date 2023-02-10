from functools import partial
from typing import Callable, Dict
from BaseClasses import CollectionState, MultiWorld
from .Regions import connect_regions
from .Items import has_items, create_item_event
from .dataType import Rule
from .regions.key import doll_regions, fnet_regions
from .regions.chapters import chapter_regions
from .regions.friends import friends_nagi_regions, friends_l_regions, friends_lao_regions, friends_gwin_regions, friends_frye_regions, \
    friends_doug_regions, friends_phog_regions, friends_elma_regions, friends_lin_regions, friends_celica_regions, \
    friends_irina_regions, friends_murderess_regions, friends_hope_regions, friends_mia_regions

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
]


def set_rules(world: MultiWorld, player: int):
    """Setting all the rules for region connections and region->item connections"""

    for regionPath in xenobladeXRegionRules:
        for rule, nextRule in zip(regionPath, regionPath[1:]):
            connect_regions(world, player, rule.region, nextRule.region, partial(
                has_items, player=player, requirements=nextRule.requirements))
