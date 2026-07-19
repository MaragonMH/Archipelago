from BaseClasses import Tutorial
from ..AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, launch_subprocess, Type
from functools import partial
from typing import cast

from .Slot import generate_slot_data
from .Items import create_items, create_item, xenobladeXItems
from .Locations import create_locations, xenobladeXLocations
from .Rules import set_rules
from .Options import XenobladeXOptions, option_groups


def launch_client(*args):
    from .Client import launch
    launch_subprocess(partial(launch, *args), name="XenobladeXClient")


components.append(Component("Xenoblade X Client", func=launch_client, component_type=Type.CLIENT,
                            game_name="Xenoblade X", supports_uri=True))


class XenobladeXWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Xenoblade Chronicles X for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Maragon", "Nina"]
    )]

    option_groups = option_groups


class XenobladeXWorld(World):
    """
     Xenoblade Chronicles X another 100+ hour game. Sounds like fun?
    """

    game = "Xenoblade X"
    topology_present = True
    web = XenobladeXWeb()

    data_version = 12
    base_id: int = 4100000

    options_dataclass = XenobladeXOptions

    item_name_to_id = (lambda b_id: {item.get_item(): b_id + item.id
                                     for item in xenobladeXItems if item.id is not None})(base_id)
    location_name_to_id = (lambda b_id: {location.get_location(): b_id + location.id
                                         for location in xenobladeXLocations.values()
                                         if location.id is not None})(base_id)

    item_name_groups = {
        prefix: {itm.get_item() for itm in xenobladeXItems if itm.prefix == prefix}
        for prefix in {itm.prefix for itm in xenobladeXItems} if prefix
    }

    def create_regions(self):
        create_locations(self)

    def create_items(self):
        create_items(self)

    def create_item(self, name: str):
        return create_item(self, name)

    def set_rules(self):
        set_rules(self)

    def generate_early(self):
        pass

    def generate_basic(self):
        pass

    def fill_slot_data(self) -> dict[str, object]:
        return generate_slot_data(cast(XenobladeXOptions, self.options))
