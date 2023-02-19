from BaseClasses import MultiWorld
from .Options import mod_options


def generate_slot_data(world: MultiWorld, player:int) -> dict[str, object]:
	slot_data: dict[str, object] = {}
	slot_data["death_link"] = getattr(world, "death_link")[player].value

	options:dict[str, str] = {}
	for path, option in mod_options.items():
		if hasattr(option, "cemu_selection_names"):
			options[path] = getattr(option, "cemu_selection_names")[getattr(world, path)[player].value]
		elif getattr(world, path)[player].value:
			options[path] = ""
	slot_data["options"] = options

	return slot_data