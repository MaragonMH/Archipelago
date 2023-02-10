import logging
from BaseClasses import Item, ItemClassification, CollectionState, MultiWorld
from .items.arts import arts_data
from .items.classes import classes_data
from .items.dataprobes import dataprobes_data
from .items.dollArmor import doll_armor_data
from .items.dollAugments import doll_augment_data
from .items.dollFrames import doll_frames_data
from .items.dollWeapons import doll_weapons_data
from .items.fieldSkills import field_skills_data
from .items.friends import friends_data
from .items.groundArmor import ground_armor_data
from .items.groundAugments import ground_augments_data
from .items.groundWeapons import ground_weapons_data
from .items.keys import keys_data
from .items.skills import skills_data
from .dataType import Requirement, GroupType
from typing import NamedTuple, Optional

class Itm(NamedTuple):
    prefix: str
    name: str
    type: int
    id: int
    progression: ItemClassification = ItemClassification.filler
    count: int = 1
    def get_item(self):
        return f"{self.prefix}: {self.name}"


class XenobladeXItem(Item):
    """A generated item"""
    game: str = "XenobladeX"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)
        if code is None: self.type = "Event"

itemTypes:dict[str, GroupType] = {
    "KEY": GroupType(0), 
    "AMR": GroupType(1, 5), 
    "WPN": GroupType(6, 2), 
    "SKF": GroupType(9), 
    "SKAMR": GroupType(0xa, 5), 
    "SKWPN": GroupType(0xf, 5), 
    "AUG": GroupType(0x14, 2), 
    "SKAUG": GroupType(0x16, 3), 
    "DP": GroupType(0x1c), 
    "ART": GroupType(0x20), 
    "SKL": GroupType(0x21), 
    "FRD": GroupType(0x22), 
    "FLDSK": GroupType(0x23), 
    "CL": GroupType(0x24), 
}

# Be careful all item_data tables are starting with index 1
xenobladeXItems = [
    *(Itm(f"KEY", e.name, itemTypes["KEY"].type, i + 1, ItemClassification.progression) for i, e in enumerate(keys_data) if e.valid),
    *(Itm(f"AMR", e.name, itemTypes["AMR"].type, i + 1) for i, e in enumerate(ground_armor_data) if e.valid), 
    *(Itm(f"WPN", e.name, itemTypes["WPN"].type, i + 1) for i, e in enumerate(ground_weapons_data) if e.valid), 
    *(Itm(f"SKF", e.name, itemTypes["SKF"].type, i + 1, ItemClassification.progression) for i, e in enumerate(doll_frames_data) if e.valid), 
    *(Itm(f"SKAMR", e.name, itemTypes["SKAMR"].type, i + 1) for i, e in enumerate(doll_armor_data) if e.valid), 
    *(Itm(f"SKWPN", e.name, itemTypes["SKWPN"].type, i + 1) for i, e in enumerate(doll_weapons_data) if e.valid), 
    *(Itm(f"AUG", e.name, itemTypes["AUG"].type, i + 1) for i, e in enumerate(ground_augments_data) if e.valid), 
    *(Itm(f"SKAUG", e.name, itemTypes["SKAUG"].type, i + 1) for i, e in enumerate(doll_augment_data) if e.valid), 
    *(Itm(f"DP", e.name, itemTypes["DP"].type, i + 1, ItemClassification.progression, e.count) for i, e in enumerate(dataprobes_data) if e.valid), 
    *(Itm(f"ART", e.name, itemTypes["ART"].type, i + 1, ItemClassification.useful) for i, e in enumerate(arts_data) if e.valid), 
    *(Itm(f"SKL", e.name, itemTypes["SKL"].type, i + 1, ItemClassification.useful) for i, e in enumerate(skills_data) if e.valid), 
    *(Itm(f"FRD", e.name, itemTypes["FRD"].type, i + 1, ItemClassification.progression, e.count) for i, e in enumerate(friends_data) if e.valid), 
    *(Itm(f"FLDSK", e.name, itemTypes["FLDSK"].type, i + 1, ItemClassification.progression, e.count) for i, e in enumerate(field_skills_data) if e.valid), 
    *(Itm(f"CL", e.name, itemTypes["CL"].type, i + 1, ItemClassification.useful) for i, e in enumerate(classes_data) if e.valid),
]

def calculate_item_type_offsets():
    for prefix, group in itemTypes.items():
        group.offset=next(i for i, item in enumerate(xenobladeXItems) if item.prefix == prefix)


def create_items(world: MultiWorld, player, base_id):
    """Create all items"""
    for abs_id, item in enumerate(xenobladeXItems, base_id):
        world.itempool += [XenobladeXItem(item.get_item(), item.progression, abs_id, player) for i in range(item.count)]


def create_item(world: MultiWorld, item_name, player, abs_id) -> Item:
    """Creates another item only used from Ap"""
    item = XenobladeXItem(item_name, ItemClassification.filler, abs_id, player)
    world.itempool += [item]
    return item


def create_item_event(world:MultiWorld, name: str, player) -> Item:
    """Create an event, which gets attached to the items"""
    event = XenobladeXItem(name, ItemClassification.useful, None, player)
    world.itempool += [event]
    return event


def has_items(state: CollectionState, player, requirements: list[Requirement]) -> bool:
    """Returns true if the state satifies the item requirements"""
    result = True
    for requirement in requirements:
        state.count
        result = result and state.has(requirement.name, player, requirement.count)
    return result

def debug_print_duplicates():
    xs = [i.name for i in xenobladeXItems]
    logging.info(set([x for x in xs if xs.count(x) > 1]))
