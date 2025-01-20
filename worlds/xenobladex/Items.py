from collections import OrderedDict
import logging
from random import sample, seed
from BaseClasses import Item, ItemClassification as ItCl, MultiWorld
from dataclasses import dataclass, replace
from typing import Dict, Generator, List, Optional


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


from .items.arts import arts_data  # noqa: E402
from .items.classes import classes_data  # noqa: E402
from .items.dataprobes import dataprobes_data  # noqa: E402
from .items.dollArmor import doll_armor_data  # noqa: E402
from .items.dollAugments import doll_augment_data  # noqa: E402
from .items.dollFrames import doll_frames_data  # noqa: E402
from .items.dollWeapons import doll_weapons_data  # noqa: E402
from .items.fieldSkills import field_skills_data  # noqa: E402
from .items.friends import friends_data  # noqa: E402
from .items.groundArmor import ground_armor_data  # noqa: E402
from .items.groundAugments import ground_augments_data  # noqa: E402
from .items.groundWeapons import ground_weapons_data  # noqa: E402
from .items.keys import keys_data  # noqa: E402
from .items.skills import skills_data  # noqa: E402


class XenobladeXItem(Item):
    """A generated item"""
    game: str = "Xenoblade X"


game_type_item_to_offset: OrderedDict[int, int] = OrderedDict()


class _Itms:
    table_size = 0
    last_table_size = 0

    @staticmethod
    def gen(prefix: str, type: int, data: list[Itm], prog: ItCl = ItCl.filler,
            type_count: int = 1) -> Generator[Itm, None, None]:
        _Itms.table_size += _Itms.last_table_size
        for typ in range(type, type + type_count):
            game_type_item_to_offset[typ] = _Itms.table_size
        _Itms.last_table_size = len(data)
        return (replace(e, type=type, id=_Itms.table_size + i + 1, prefix=prefix,
                        progression=prog, type_count=type_count)
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


def create_items(world: MultiWorld, player, base_id, options, item_name_to_id: Dict[str, int]):
    """Create all items"""
    itempool: List[Item] = []
    # Add all important Items, these are always added to the item pool
    for item in xenobladeXImportantItems:
        itempool += [XenobladeXItem(item.get_item(), item.progression, base_id + item.id, player)
                     for _ in range(item.count)]

    # Add all optional Items to the item pool
    # Add all optional Items to the item pool, these are selected at random,
    # depending on how many slots are left in the location pool
    selected_optional_items: list[Itm] = [item for item in xenobladeXOptionalItems
                                          if item.prefix is not None and getattr(options, item.prefix.lower()).value]
    # Keep enough space for the victory item_event
    total_locations = len(world.get_unfilled_locations(player)) - 1
    missing_item_count: int = min(total_locations - len(itempool), len(selected_optional_items))
    seed(world.seed)
    random_items: list[Itm] = sample(selected_optional_items, missing_item_count)
    for item in xenobladeXOptionalItems:
        if item not in random_items:
            continue
        itempool += [XenobladeXItem(item.get_item(), item.progression, base_id + item.id, player)
                     for _ in range(item.count)]
    world.itempool += itempool

    world.itempool += [create_filler(player, item_name_to_id) for _ in range(total_locations - len(itempool))]


def create_item(item_name: str, player: int, abs_id: int, is_prog: bool = True) -> XenobladeXItem:
    """Create another item"""
    return XenobladeXItem(item_name, ItCl.progression if is_prog else ItCl.filler, abs_id, player)


def create_filler(player: int, item_name_to_id: Dict[str, int]) -> XenobladeXItem:
    return create_item("KEY: Filler", player, item_name_to_id["KEY: Filler"], is_prog=False)


def debug_print_duplicates():
    xs = [i.get_item() for i in xenobladeXItems]
    dup = {x: xs.count(x) for x in xs if xs.count(x) > 1}
    for name, n in dup.items():
        logging.debug(f"Duplicate: {name}, Count: {n}")
