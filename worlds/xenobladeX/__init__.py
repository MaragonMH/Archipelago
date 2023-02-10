import typing
from .Options import xenobladeX_options
from .Locations import xenobladeXLocations
from .Items import xenobladeXItems, create_items
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Tutorial
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
    """ #Lifted from Store Page

    game: str = "XenobladeX"
    topology_present = False
    web = XenobladeXWeb()

    data_version = 0
    item_base_id = 4001000
    location_base_id = 4101000

    option_definitions = xenobladeX_options

    def _createData(data, baseId):
        result = {}
        id = baseId
        for xenobladeXItemGroup in xenobladeXItems.values():
            for name, item in xenobladeXItemGroup.items():
                count = item["count"] if "count" in item else 1
                for idx in range(count):
                    appendix = " #" + str(idx) if idx > 1 else ""
                    result[name + appendix] = id
                    id += 1
        return result

    print(_createData(xenobladeXItems, item_base_id))
    item_name_to_id = _createData(xenobladeXItems, item_base_id)
    location_name_to_id = _createData(xenobladeXLocations, location_base_id)

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.location_name_to_id)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_items(self):
        create_items(self)
