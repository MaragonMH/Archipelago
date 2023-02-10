from BaseClasses import Tutorial
from .Slot import generate_slot_data
from .Items import create_filler, xenobladeXItems, create_items, create_item
from .Rules import set_rules
from .Locations import create_locations, xenobladeXLocations
from .Options import xenobladeX_options
from ..AutoWorld import World, WebWorld


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

    def _generate_lookup(self, data, b_id:int):
        return { e.get_item(): b_id + e.id for e in data}

    item_name_to_id = { item.get_item(): sum(b_id, item.id) for b_id in enumerate(range(1), base_id) for item in xenobladeXItems} 
    location_name_to_id = { location.get_location(): sum(b_id, location.id) for b_id in enumerate(range(1), base_id) for location in xenobladeXLocations }

    def create_regions(self):
        create_locations(self.multiworld, self.player, self.base_id, self.location_name_to_id)

    def create_items(self):
        create_items(self.multiworld, self.player, self.base_id)

    def create_item(self, name: str):
        create_item(self.multiworld, name, self.player, self.item_name_to_id[name])

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.item_name_to_id)

    def generate_early(self):
        pass

    def generate_basic(self):
        create_filler(self.multiworld, self.player, self.item_name_to_id)

    def fill_slot_data(self) -> dict[str, object]:
        return generate_slot_data(self.base_id, self.multiworld, self.player)