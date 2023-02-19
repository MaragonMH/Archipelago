from BaseClasses import MultiWorld
from .Locations import create_location
from .Items import create_item_event

def set_rules(world: MultiWorld, player: int, item_name_to_id, location_name_to_id):
    """Setting all the rules for region connections and region->item connections"""
    create_location(world, "Epilogue", "EBK: Lao", player, location_name_to_id["EBK: Lao"])
    world.get_location("EBK: Lao", player).place_locked_item(
        create_item_event("KEY: Victory", player, item_name_to_id["KEY: Victory"]))
    world.completion_condition[player] = lambda state: state.has("KEY: Victory", player)
