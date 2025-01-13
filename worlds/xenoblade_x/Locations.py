from collections import OrderedDict
from BaseClasses import Location, MultiWorld
from dataclasses import dataclass, field, replace
from typing import Generator, Optional
from .Regions import add_region_location, init_region

@dataclass(frozen=True)
class Loc:
    name: str
    valid: bool = True
    count: int = 1
    regions: list[str] = field(default_factory=lambda: ['Menu'])
    type: Optional[int] = None
    id: Optional[int] = None
    prefix: Optional[str] = None
    def get_location(self):
        return f"{self.prefix}: {self.name}"
    def get_region(self):
        return "+".join(sorted(self.regions))

from .locations.collepedia import collepedia_data
from .locations.enemies import enemies_data
from .locations.fnNodes import fn_nodes_data
from .locations.locations import locations_data
from .locations.segments import segments_data

class XenobladeXLocation(Location):
    game: str = "XenobladeX"

game_type_location_to_offset:OrderedDict[int, int] = OrderedDict()

def _genLocs(prefix:str, type:int, data:list[Loc]) -> Generator[Loc, None, None]:
    _genLocs.table_size += _genLocs.last_table_size
    game_type_location_to_offset[type] = _genLocs.table_size
    _genLocs.last_table_size = len(data)
    return (replace(e, type=type, id=_genLocs.table_size + i + 1, prefix=prefix) for i, e in enumerate(data) if e.valid)
_genLocs.table_size = 0
_genLocs.last_table_size = 0

xenobladeXLocations = [
    *_genLocs("CLP", 0, collepedia_data),
    *_genLocs("EBK", 1, enemies_data),
    *_genLocs("FNO", 2, fn_nodes_data),
    *_genLocs("SEG", 3, segments_data),
    *_genLocs("LOC", 4, locations_data),
]

def create_location(world:MultiWorld, region_name:str, location_name:str, player:int, abs_id:Optional[int]):
    init_region(world, player, region_name)
    return add_region_location(world, player, region_name, XenobladeXLocation(player, 
        location_name, abs_id, world.get_region(region_name, player)))

def create_locations(world:MultiWorld, player:int, base_id:int, location_name_to_id):
    for location in xenobladeXLocations:
        if location.prefix is None or location.id is None: continue
        if hasattr(world, location.prefix) and not getattr(world, location.prefix)[player].value: continue
        create_location(world, location.get_region(), location.get_location(), player, base_id + location.id)
