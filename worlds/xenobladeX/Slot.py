from typing import Dict

from BaseClasses import MultiWorld
from .Options import mod_options, NamedChoice
from .Items import xenobladeXItems, itemTypes
from .Locations import xenobladeXLocations


def generate_slot_data(base_id: int, world: MultiWorld, player:int) -> Dict[str, object]:
	item_types = { item.type for item in xenobladeXItems}
	location_types = { location.type for location in xenobladeXLocations}

	options:Dict[str, str] = {}
	for path, option in mod_options.items():
		if hasattr(option, "cemu_selection_names"):
			options[path] = option.cemu_selection_names[getattr(world, path)[player].value]
		elif getattr(world, path)[player].value:
			options[path] = ""
		

	item_lookup = { item_type: {} for item_type in item_types }
	location_lookup = { location_type: {} for location_type in location_types }

	for id, item in enumerate(xenobladeXItems, base_id):
		for i in range(itemTypes[item.prefix].count):
			if item.type + i not in item_lookup: item_lookup[item.type + i] = {}
			item_lookup[item.type + i][item.id] = id

	for id, location in enumerate(xenobladeXLocations, base_id):
		if location.type not in location_lookup: item_lookup[location.type] = {}
		location_lookup[location.type][location.id] = id

	slot_data: Dict[str, object] = {}
	slot_data["base_id"] = base_id
	slot_data["options"] = options
	slot_data["archipelago_item_to_name"] = {id: item.get_item() for id, item in enumerate(xenobladeXItems, base_id)}
	slot_data["archipelago_item_to_game_item"] = [(item.type, item.id) for item in xenobladeXItems]
	slot_data["game_type_item_to_archipelago_item"] = item_lookup
	slot_data["game_type_location_to_archipelago_location"] = location_lookup
	return slot_data