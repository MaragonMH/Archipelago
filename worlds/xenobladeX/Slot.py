from typing import Dict
from .Items import xenobladeXItems, itemTypes
from .Locations import xenobladeXLocations

def generate_slot_data(base_id: int) -> Dict[str, object]:
	item_types = { item.type for item in xenobladeXItems}
	location_types = { location.type for location in xenobladeXLocations}

	item_lookup = { item_type: {} for item_type in item_types }
	location_lookup = { location_type: {} for location_type in location_types }

	for id, item in enumerate(xenobladeXItems, base_id):
		for i in range(itemTypes[item.prefix].count):
			item_lookup[item.type + i][item.id] = id
	for id, location in enumerate(xenobladeXLocations, base_id):
		location_lookup[location.type][location.id] = id

	slot_data: Dict[str, object] = {}
	slot_data["base_id"] = base_id
	slot_data["archipelago_item_to_name"] = {id: f"{item.prefix}: {item}" for id, item in enumerate(xenobladeXItems, base_id)}
	slot_data["archipelago_item_to_game_item"] = [(item.type, item.id) for item in xenobladeXItems]
	slot_data["game_type_item_to_archipelago_item"] = item_lookup
	slot_data["game_type_location_to_archipelago_location"] = location_lookup
	return slot_data