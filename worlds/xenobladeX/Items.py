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
from .dataType import Requirement
from typing import NamedTuple, Optional

class Itm(NamedTuple):
    prefix: str
    name: str
    type: int
    id: int
    progression: ItemClassification = ItemClassification.filler


class XenobladeXItem(Item):
    """A generated item"""
    game: str = "XenobladeX"

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        super().__init__(name, classification, code, player)
        if code is None: self.type = "Event" 

xenobladeXItems = [
    *(Itm(f"KEY: ", e.name, 0, i + 1, ItemClassification.progression) for i, e in enumerate(keys_data) if e.valid),
    *(Itm(f"AMR: ", e.name, 1, i + 1) for i, e in enumerate(ground_armor_data) if e.valid), 
    *(Itm(f"WPN: ", e.name, 6, i + 1) for i, e in enumerate(ground_weapons_data) if e.valid), 
    *(Itm(f"SKF: ", e.name, 9, i + 1, ItemClassification.progression) for i, e in enumerate(doll_frames_data) if e.valid), 
    *(Itm(f"SKAUG: ", e.name, 0xa, i + 1) for i, e in enumerate(doll_armor_data) if e.valid), 
    *(Itm(f"SKWPN: ", e.name, 0xf, i + 1) for i, e in enumerate(doll_weapons_data) if e.valid), 
    *(Itm(f"AUG: ", e.name, 0x14, i + 1) for i, e in enumerate(ground_augments_data) if e.valid), 
    *(Itm(f"SKAUG: ", e.name, 0x16, i + 1) for i, e in enumerate(doll_augment_data) if e.valid), 
    *(Itm(f"DP: ", e.name, 0x1c, i + 1, ItemClassification.progression) for i, e in enumerate(dataprobes_data) for c in range(e.count) if e.valid), 
    *(Itm(f"ART: ", e.name, 0x20, i + 1, ItemClassification.useful) for i, e in enumerate(arts_data) if e.valid), 
    *(Itm(f"SKL: ", e.name, 0x21, i + 1, ItemClassification.useful) for i, e in enumerate(skills_data) if e.valid), 
    *(Itm(f"FRD: ", e.name, 0x22, i + 1, ItemClassification.progression) for i, e in enumerate(friends_data) for c in range(e.count) if e.valid), 
    *(Itm(f"FLDSK: ", e.name, 0x23, i + 1, ItemClassification.progression) for i, e in enumerate(field_skills_data) for c in range(e.count) if e.valid), 
    *(Itm(f"CL: ", e.name, 0x24, i + 1, ItemClassification.useful) for i, e in enumerate(classes_data) if e.valid),
]


def create_items(world: MultiWorld, player, base_id):
    """Create all items"""
    for abs_id, item in enumerate(xenobladeXItems, base_id):
        world.itempool += [XenobladeXItem(item.prefix + item.name, item.progression, abs_id, player)]


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
        result = result and state.has(requirement.name, player, requirement.count)
    return result

def debug_print_duplicates():
    xs = [i.name for i in xenobladeXItems]
    logging.info(set([x for x in xs if xs.count(x) > 1]))
