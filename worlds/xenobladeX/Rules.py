from __future__ import annotations
from functools import partial
from ..generic.Rules import add_rule
from .Regions import connect_regions
from .Items import has_items, get_generated_item_by_name

# Requirements to reach this region
# Use dict to specify the quantity you need
xenobladeXRegionRules = {
    "Chapter 1": {},
    "Chapter 2": {},
    "Chapter 3": {},
    "Chapter 4": {},
    "Chapter 5": {
        "Mining G1": {"count": 3},
        "Research G1": {"count": 1},
        "Frontier Nav": {}
    },
    "Chapter 6": {},
    "Chapter 7": {},
    "Chapter 8": {},
    "Chapter 9": {"Lao Heart": {"count": 1}},
    "Chapter 10": {},
    "Chapter 11": {},
    "Chapter 12": {"Gwin Heart": {"count": 1}},
    "Epilogue": {"Skell License": {}, "Skell Flight Module": {}}
}

# Specifiy a location and a list of required items
# Use dict for count
# Use Array for or rules
# Big TODO
xenobladeXRules = {
    "FN Site 102 (2, 7, -9)": [{"Frontier Nav": {}}],
}


def set_rules(world, player):
    """Setting all the rules for region connections and region->item connections"""
    # supposed to use create_event, but that crashes with this version
    # victoryEvent = create_event("Victory")
    victory_event = get_generated_item_by_name("Victory")
    victory_location = world.get_location("Final Boss", player)
    victory_location.place_locked_item(victory_event)
    world.completion_condition[player] = lambda state: state.has(
        "Victory", player)

    last_chapter = "Menu"
    for chapter, requirements in xenobladeXRegionRules.items():
        # Region connection. Only for advancing chapters
        connect_regions(world, player, last_chapter, chapter, partial(
            has_items, player=player, requirements=requirements))
        last_chapter = chapter

    for (location, rules) in xenobladeXRules.items():
        for requirements in rules:
            # Location connection. Further requirements, if the chapter criteria is fullfilled
            add_rule(world.get_location(location, player), partial(
                has_items, player=player, requirements=requirements))
