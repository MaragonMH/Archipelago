import re
from collections import Counter, OrderedDict
from BaseClasses import Location
from Options import Option
from dataclasses import replace
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from . import XenobladeXWorld

from . import Regions

from .locations import Loc
from .locations.collepedia import collepedia_data
from .locations.enemies import enemies_data
from .locations.fnNodes import fn_nodes_data
from .locations.locations import locations_data
from .locations.segments import segments_data
from .locations.tmp import tmp_data
# from .locations.quests import quests_data
# from .locations.shops import shops_data


class XenobladeXLocation(Location):
    game: str = "Xenoblade X"


game_type_location_to_offset: OrderedDict[int, int] = OrderedDict()


class _Locs:
    table_size = 0
    last_table_size = 0

    @staticmethod
    def gen(prefix: str, type: int, data: list[Loc]) -> dict[str, Loc]:
        _Locs.table_size += _Locs.last_table_size
        game_type_location_to_offset[type] = _Locs.table_size
        _Locs.last_table_size = len(data)
        return {f"{prefix}: {e.name}": replace(e, type=type, id=_Locs.table_size + i + 1, prefix=prefix)
                for i, e in enumerate(data) if e.valid}


xenobladeXLocations = {
    **_Locs.gen("CLP", 0, collepedia_data),
    **_Locs.gen("EBK", 1, enemies_data),
    **_Locs.gen("FNO", 2, fn_nodes_data),
    **_Locs.gen("SEG", 3, segments_data),
    **_Locs.gen("LOC", 4, locations_data),
    **_Locs.gen("TMP", 5, tmp_data),
    # **_Locs.gen("QST", 5, quests_data),
    # **_Locs.gen("SHP", 6, shops_data),
}


def compress_rules(rules: list[str]) -> list[str]:
    new_rules = list(set(rules))
    if "Blade License" in new_rules and ("Flight Module" in new_rules or "Skell License" in new_rules):
        new_rules.remove("Blade License")
    if "Skell License" in new_rules and "Flight Module" in new_rules:
        new_rules.remove("Skell License")
    rule_lvls = [[match.group(1).strip(), int(match.group(2)) if match.group(2) else 0]
                 for match in (re.fullmatch(r"^(.+?)(?: (\d+)?)?$", rule) for rule in new_rules) if match]
    compressed: list[str] = []
    highest: dict[str, int] = {}
    for rule_lvl in rule_lvls:
        name = str(rule_lvl[0])
        lvl = int(rule_lvl[1])
        if rule_lvl[1] == 0:
            compressed.append(name)
        else:
            if rule_lvl[0] in highest:
                highest[rule_lvl[0]] = max(lvl, highest[name])
            else:
                highest[name] = lvl
    result = sorted(compressed + [f"{name} {lvl}" for name, lvl in highest.items()])
    return result


def _resolve_dependencies() -> None:
    dependency_lookup: dict[str, str] = {}
    for loc in xenobladeXLocations.values():
        dependency = loc.name.split(" - ")[0]
        if dependency not in loc.depends:
            assert dependency not in dependency_lookup, f"Location dependency is not unique: {dependency}"
            dependency_lookup[dependency] = loc.get_location()

    for loc in xenobladeXLocations.values():
        dependencies = loc.depends.copy()
        rules: list[str] = loc.rules.copy()
        while True:
            if len(dependencies) < 1:
                break
            dependency = dependencies.pop()
            assert dependency in dependency_lookup, f"Location dependency {dependency} is not available:"
            dep_loc = xenobladeXLocations[dependency_lookup[dependency]]
            dependencies += dep_loc.depends
            rules += dep_loc.rules
        xenobladeXLocations[loc.get_location()] = replace(loc, rules=compress_rules(rules), depends=[])


_resolve_dependencies()


def create_location(world: "XenobladeXWorld", region_name: str, location_name: str):
    Regions.init_region(world, region_name)
    assert location_name in xenobladeXLocations, f"{location_name} not in locations"
    location_id = xenobladeXLocations[location_name].id
    assert location_id is not None, f"{location_name} has no id"
    id = world.base_id + location_id
    return Regions.add_region_location(world, region_name, XenobladeXLocation(world.player, location_name,
                                                                              id, world.get_region(region_name)))


def create_locations(world: "XenobladeXWorld"):
    for location in xenobladeXLocations.values():
        if location.prefix is None or location.id is None:
            continue
        location_option: Optional[Option] = getattr(world.options, location.prefix.lower(), None)
        if location.required or location_option is None or location_option.value:
            create_location(world, "Menu", location.get_location())
