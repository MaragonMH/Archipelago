from __future__ import annotations
from BaseClasses import Tutorial
from .Items import xenobladeXItems, create_items, create_item, create_data, create_item_event
from .Rules import set_rules
from .Regions import create_regions
from .Locations import xenobladeXLocations, create_location_event
from .Options import xenobladeX_options
from ..AutoWorld import World, WebWorld


class XenobladeXWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Xenoblade Chronicles X for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["MaragonMH"]
    )]


class XenobladeXWorld(World):
    """
     Xenoblade Chronicles X another 100+ hour game. Sounds like fun?
    """  # Lifted from Store Page

    game: str = "XenobladeX"
    topology_present = True
    web = XenobladeXWeb()

    data_version = 0
    base_id = 4001000

    option_definitions = xenobladeX_options

    item_name_to_id = create_data(xenobladeXItems, base_id)
    location_name_to_id = create_data(xenobladeXLocations, base_id)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.location_name_to_id)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_items(self):
        create_items(self.multiworld, self.player, self.base_id)

    def create_item(self, name: str):
        create_item(self.multiworld, name, self.player, self.base_id)
