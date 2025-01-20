from collections import OrderedDict
from BaseClasses import Location, MultiWorld
from dataclasses import dataclass, field, replace
from typing import Generator, Optional
from .Regions import add_region_location, init_region


@dataclass(frozen=True)
class Loc:
    name: str
    valid: bool = True
    regions: list[str] = field(default_factory=lambda: ['Menu'])
    type: Optional[int] = None
    id: Optional[int] = None
    prefix: Optional[str] = None

    def get_location(self):
        return f"{self.prefix}: {self.name}"

    def get_region(self):
        return "+".join(sorted(self.regions))


from .locations.collepedia import collepedia_data  # noqa: E402
from .locations.enemies import enemies_data  # noqa: E402
from .locations.fnNodes import fn_nodes_data  # noqa: E402
from .locations.locations import locations_data  # noqa: E402
from .locations.segments import segments_data  # noqa: E402


class XenobladeXLocation(Location):
    game: str = "Xenoblade X"


game_type_location_to_offset: OrderedDict[int, int] = OrderedDict()


class _Locs:
    table_size = 0
    last_table_size = 0

    @staticmethod
    def gen(prefix: str, type: int, data: list[Loc]) -> Generator[Loc, None, None]:
        _Locs.table_size += _Locs.last_table_size
        game_type_location_to_offset[type] = _Locs.table_size
        _Locs.last_table_size = len(data)
        return (replace(e, type=type, id=_Locs.table_size + i + 1, prefix=prefix)
                for i, e in enumerate(data) if e.valid)


xenobladeXLocations = [
    *_Locs.gen("CLP", 0, collepedia_data),
    *_Locs.gen("EBK", 1, enemies_data),
    *_Locs.gen("FNO", 2, fn_nodes_data),
    *_Locs.gen("SEG", 3, segments_data),
    *_Locs.gen("LOC", 4, locations_data),
]


def create_location(world: MultiWorld, region_name: str, location_name: str, player: int, abs_id: Optional[int]):
    init_region(world, player, region_name)
    return add_region_location(world, player, region_name,
                               XenobladeXLocation(player, location_name, abs_id, world.get_region(region_name, player)))


def create_locations(world: MultiWorld, player: int, base_id: int):
    for location in xenobladeXLocations:
        if location.prefix is None or location.id is None:
            continue
        if hasattr(world, location.prefix) and not getattr(world, location.prefix)[player].value:
            continue
        create_location(world, location.get_region(), location.get_location(), player, base_id + location.id)
