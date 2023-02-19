from BaseClasses import Tutorial
from ..AutoWorld import World, WebWorld
from .Slot import generate_slot_data
from .Regions import init_region
from .Items import create_filler, xenobladeXItems, create_items, create_item
from .Rules import set_rules
from .Locations import create_locations, xenobladeXLocations
from .Options import xenobladeX_options


class XenobladeXWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Xenoblade Chronicles X for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Maragon"]
    )]


class XenobladeXWorld(World):
    """
     Xenoblade Chronicles X another 100+ hour game. Sounds like fun?
    """

    game: str = "XenobladeX"
    topology_present = True
    web = XenobladeXWeb()

    data_version = 0
    base_id = 4100000

    option_definitions = xenobladeX_options

    item_name_to_id = (lambda b_id=base_id: { item.get_item(): b_id + item.id for item in xenobladeXItems if item.id is not None})()
    location_name_to_id = (lambda b_id=base_id: { location.get_location(): b_id + location.id for location in xenobladeXLocations if location.id is not None})()

    def create_regions(self):
        init_region(self.multiworld, self.player, "Menu")
        create_locations(self.multiworld, self.player, self.base_id, self.location_name_to_id)

    def create_items(self):
        create_items(self.multiworld, self.player, self.base_id)

    def create_item(self, name: str):
        create_item(self.multiworld, name, self.player, self.item_name_to_id[name])

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.item_name_to_id, self.location_name_to_id)

    def generate_early(self):
        pass

    def generate_basic(self):
        create_filler(self.multiworld, self.player, self.item_name_to_id)

    def fill_slot_data(self) -> dict[str, object]:
        return generate_slot_data(self.multiworld, self.player)