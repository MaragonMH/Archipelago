from BaseClasses import MultiWorld
from .Options import mod_options
from .Items import itemTypes
from .Locations import locTypes


def generate_slot_data(base_id: int, world: MultiWorld, player:int) -> dict[str, object]:
	slot_data: dict[str, object] = {}
	slot_data["death_link_enabled"] = getattr(world, "death_link")[player].value

	item_types = { item.type + count: base_id + item.offset for item in itemTypes for count in range(item.count)}
	location_types = { location.type + count: base_id + location.offset for location in locTypes for count in range(location.count)}
	slot_data["game_type_item_to_offset"] = item_types
	slot_data["game_type_location_to_offset"] = location_types

	options:dict[str, str] = {}
	for path, option in mod_options.items():
		if hasattr(option, "cemu_selection_names"):
			options[path] = getattr(option, "cemu_selection_names")[getattr(world, path)[player].value]
		elif getattr(world, path)[player].value:
			options[path] = ""
	slot_data["options"] = options

	return slot_data