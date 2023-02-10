import logging
from BaseClasses import Item, ItemClassification as ItCl, CollectionState, MultiWorld
from random import sample, seed
from .Locations import additionalLocNames
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
from .dataType import Data, Requirement, GroupType
from typing import Generator, NamedTuple, Optional

class Itm(NamedTuple):
    prefix: str
    name: str
    type: int
    id: int
    progression: ItCl = ItCl.filler
    count: int = 1
    type_count:int = 1
    def get_item(self):
        return f"{self.prefix}: {self.name}"

class XenobladeXItem(Item):
    """A generated item"""
    game: str = "XenobladeX"

itemTypes:list[GroupType] = []

def _generateItems(prefix:str, type:int, data:list[Data], prog:ItCl=ItCl.filler, type_count:int = 1) -> Generator[Itm, None, None]:
    offset = itemTypes[-1].offset + itemTypes[-1].length if itemTypes else 0
    itemTypes.append(GroupType(prefix, type, offset, len(data), type_count))
    return (Itm(prefix, e.name, type, offset + i + 1, prog, e.count, type_count) for i, e in enumerate(data) if e.valid)

xenobladeXImportantItems = [
    *_generateItems("KEY", type=0, data=keys_data, prog=ItCl.progression),
    *_generateItems("SKF", type=9, data=doll_frames_data, prog=ItCl.progression), 
    *_generateItems("DP", type=0x1c, data=dataprobes_data, prog=ItCl.progression), 
    *_generateItems("ART", type=0x20, data=arts_data, prog=ItCl.useful), 
    *_generateItems("SKL", type=0x21, data=skills_data, prog=ItCl.useful), 
    *_generateItems("FRD", type=0x22, data=friends_data, prog=ItCl.progression), 
    *_generateItems("FLDSK", type=0x23, data=field_skills_data, prog=ItCl.progression), 
    *_generateItems("CL", type=0x24, data=classes_data, prog=ItCl.useful),
]

xenobladeXOptionalItems = [
    *_generateItems("AMR", type=1, type_count=5, data=ground_armor_data), 
    *_generateItems("WPN", type=6, type_count=2, data=ground_weapons_data), 
    *_generateItems("SKAMR", type=0xa, type_count=5, data=doll_armor_data), 
    *_generateItems("SKWPN", type=0xf, type_count=5, data=doll_weapons_data), 
    *_generateItems("AUG", type=0x14, type_count=2, data=ground_augments_data), 
    *_generateItems("SKAUG", type=0x16, type_count=3, data=doll_augment_data), 
]

xenobladeXItems = [
    *xenobladeXImportantItems,
    *xenobladeXOptionalItems,
]

def create_items(world: MultiWorld, player, base_id):
    """Create all items"""
    for item in xenobladeXImportantItems:
        world.itempool += [XenobladeXItem(item.get_item(), item.progression, base_id + item.id, player) for i in range(item.count)]

    selected_optional_items:list[Itm] = [item for item in xenobladeXOptionalItems if getattr(world, item.prefix)[player].value]
    missing_item_count:int = min(len(world.get_locations()) - len(additionalLocNames) - len(world.get_items()), len(selected_optional_items))
    seed(world.seed)
    random_items:list[Itm] = sample(selected_optional_items, missing_item_count)
    for item in xenobladeXOptionalItems:
        if item not in random_items: continue
        world.itempool += [XenobladeXItem(item.get_item(), item.progression, base_id + item.id, player) for i in range(item.count)]


def create_item(world: MultiWorld, item_name:str, player:int, abs_id:int, is_prog:bool = True) -> Item:
    """Create another item"""
    item = XenobladeXItem(item_name, ItCl.progression if is_prog else ItCl.filler, abs_id, player)
    world.itempool += [item]
    return item


def create_filler(world: MultiWorld, player:int, item_name_to_id):
    for _ in range(len(world.get_locations()) - len(world.get_items())):
        create_item(world, "KEY: Filler", player, item_name_to_id["KEY: Filler"], is_prog=False)


def create_item_event(name: str, player:int, abs_id:Optional[int] = None, is_prog:bool = True) -> Item:
    """Create an event"""
    return XenobladeXItem(name, ItCl.progression if is_prog else ItCl.filler, abs_id, player)


def has_items(state: CollectionState, player, requirements: list[Requirement]) -> bool:
    """Returns true if the state satifies the item requirements"""
    result = True
    for requirement in requirements:
        state.count
        result = result and state.has(requirement.name, player, requirement.count)
    return result

def debug_print_duplicates():
    xs = [i.get_item() for i in xenobladeXItems]
    dup = {x:xs.count(x) for x in xs if xs.count(x) > 1}
    for name, n in dup.items():
        logging.debug(f"Duplicate: {name}, Count: {n}")
