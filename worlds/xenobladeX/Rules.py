from __future__ import annotations
from functools import partial
from ..generic.Rules import add_rule
from .Locations import create_location_event
from .Regions import connect_regions
from .Items import has_items, create_item_event

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

    # Testin code here, because it does not work
    # victory_item= get_generated_item_by_name("Victory")
    # victory_item = create_item_event(world, "Victory", player)
    # world.get_location("Final Boss", self.player).place_locked_item(victory_item)
    # victory_item_event = create_item_event(world, "VICTORY", player)
    # final_boss_location_event = create_location_event(world, "Epilogue", "FINAL BOSS", player)
    # final_boss_location_event.place_locked_item(victory_item_event)
    # world.completion_condition[player] = lambda state: state.has("VICTORY", player) or state.has("Victory", player)
    world.completion_condition[player] = lambda state: state.has("Skell License", player) or state.has("Skell Flight Module", player)

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
