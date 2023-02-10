import typing
import os, json
from .Items import item_table, XenobladeXItem
from .Locations import location_table, XenobladeXLocation
from .Options import xenobladeX_options
from .Rules import set_rules
from .Regions import create_regions
from BaseClasses import Item, ItemClassification, Tutorial
from ..AutoWorld import World, WebWorld

client_version = 1


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

    item_name_to_id = item_table
    location_name_to_id = location_table

    data_version = 1

    area_connections: typing.Dict[int, int]
    area_cost_map: typing.Dict[int,int]

    music_map: typing.Dict[int,int]

    option_definitions = xenobladeX_options

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def set_rules(self):
        self.area_connections = {}
        self.area_cost_map = {}
        set_rules(self.multiworld, self.player, self.area_connections, self.area_cost_map)

    def create_item(self, name: str) -> Item:
        return XenobladeXItem(name, ItemClassification.progression, item_table[name], self.player)

    def generate_basic(self):
        trinkets = [self.create_item("Trinket " + str(i+1).zfill(2)) for i in range(0,20)]
        self.multiworld.itempool += trinkets

        musiclist_o = [1,2,3,4,9,12]
        musiclist_s = musiclist_o.copy()
        if self.multiworld.MusicRandomizer[self.player].value:
            self.multiworld.random.shuffle(musiclist_s)
        self.music_map = dict(zip(musiclist_o, musiclist_s))

    def fill_slot_data(self):
        return {
            "MusicRando": self.music_map,
            "AreaRando": self.area_connections,
            "DoorCost": self.multiworld.DoorCost[self.player].value,
            "AreaCostRando": self.area_cost_map,
            "DeathLink": self.multiworld.death_link[self.player].value,
            "DeathLink_Amnesty": self.multiworld.DeathLinkAmnesty[self.player].value
        }

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name] : item_table[i.item.name] for i in self.multiworld.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apXenobladeX"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)
