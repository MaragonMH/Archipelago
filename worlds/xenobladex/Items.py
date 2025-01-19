from collections import OrderedDict
import logging
from BaseClasses import Item, ItemClassification as ItCl, MultiWorld
from dataclasses import dataclass, replace
from typing import Generator, Optional


@dataclass(frozen=True)
class Itm:
    name: str
    valid: bool = True
    count: int = 1
    type: Optional[int] = None
    id: Optional[int] = None
    prefix: Optional[str] = None
    progression: ItCl = ItCl.filler
    type_count: int = 1

    def get_item(self):
        if self.prefix is None:
            return self.name
        return f"{self.prefix}: {self.name}"

# flake8: noqa: E402
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


class XenobladeXItem(Item):
    """A generated item"""
    game: str = "XenobladeX"


game_type_item_to_offset: OrderedDict[int, int] = OrderedDict()


class _Itms:
    table_size = 0
    last_table_size = 0

    @staticmethod
    def gen(prefix: str, type: int, data: list[Itm], prog: ItCl = ItCl.filler, type_count: int = 1) -> Generator[Itm, None, None]:
        _Itms.table_size += _Itms.last_table_size
        for typ in range(type, type + type_count):
            game_type_item_to_offset[typ] = _Itms.table_size
        _Itms.last_table_size = len(data)
        return (replace(e, type=type, id=_Itms.table_size + i + 1, prefix=prefix, progression=prog, type_count=type_count)
                for i, e in enumerate(data) if e.valid)


xenobladeXImportantItems = [
    *_Itms.gen("KEY", type=0, data=keys_data, prog=ItCl.progression),
    *_Itms.gen("SKF", type=9, data=doll_frames_data, prog=ItCl.progression),
    *_Itms.gen("DP", type=0x1c, data=dataprobes_data, prog=ItCl.progression),
    *_Itms.gen("ART", type=0x20, data=arts_data, prog=ItCl.useful),
    *_Itms.gen("SKL", type=0x21, data=skills_data, prog=ItCl.useful),
    *_Itms.gen("FRD", type=0x22, data=friends_data, prog=ItCl.progression),
    *_Itms.gen("FLDSK", type=0x23, data=field_skills_data, prog=ItCl.progression),
    *_Itms.gen("CL", type=0x24, data=classes_data, prog=ItCl.useful),
]

xenobladeXOptionalItems = [
    *_Itms.gen("AMR", type=1, type_count=5, data=ground_armor_data),
    *_Itms.gen("WPN", type=6, type_count=2, data=ground_weapons_data),
    *_Itms.gen("SKAMR", type=0xa, type_count=5, data=doll_armor_data),
    *_Itms.gen("SKWPN", type=0xf, type_count=5, data=doll_weapons_data),
    *_Itms.gen("AUG", type=0x14, type_count=2, data=ground_augments_data),
    *_Itms.gen("SKAUG", type=0x16, type_count=3, data=doll_augment_data),
]

xenobladeXItems = [
    *xenobladeXImportantItems,
    *xenobladeXOptionalItems,
]


def create_items(world: MultiWorld, player, base_id, options):
    """Create all items"""
    # Add all important Items, these are always added to the item pool
    for item in xenobladeXImportantItems:
        world.itempool += [XenobladeXItem(item.get_item(), item.progression, base_id + item.id, player) for _ in range(item.count)]

    # Add all optional Items to the item pool
    for item in xenobladeXOptionalItems:
        if item.prefix is not None and getattr(options, item.prefix.lower()).value:
            world.itempool += [XenobladeXItem(item.get_item(), item.progression, base_id + item.id, player) for _ in range(item.count)]


def create_item(world: MultiWorld, item_name: str, player: int, abs_id: int, is_prog: bool = True) -> XenobladeXItem:
    """Create another item"""
    item = XenobladeXItem(item_name, ItCl.progression if is_prog else ItCl.filler, abs_id, player)
    world.itempool += [item]
    return item


def create_filler(world: MultiWorld, player: int, item_name_to_id) -> XenobladeXItem:
    return create_item(world, "KEY: Filler", player, item_name_to_id["KEY: Filler"], is_prog=False)


def create_item_event(name: str, player: int, abs_id: Optional[int] = None, is_prog: bool = True) -> XenobladeXItem:
    """Create an event"""
    return XenobladeXItem(name, ItCl.progression if is_prog else ItCl.filler, abs_id, player)


def debug_print_duplicates():
    xs = [i.get_item() for i in xenobladeXItems]
    dup = {x: xs.count(x) for x in xs if xs.count(x) > 1}
    for name, n in dup.items():
        logging.debug(f"Duplicate: {name}, Count: {n}")
