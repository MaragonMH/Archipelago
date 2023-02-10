from BaseClasses import Location, MultiWorld
from .dataType import GroupType, LocData
from .locations.collepedia import collepedia_data
from .locations.enemies import enemies_data
from .locations.fnNodes import fn_nodes_data
from .locations.locations import locations_data
from .locations.segments import segments_data
from .Regions import add_region_location, init_region
from typing import Generator, NamedTuple, Optional

class Loc(NamedTuple):
    prefix: str
    name: str
    type: int
    id: int
    regions: list[str]
    count: int
    def get_location(self):
        return f"{self.prefix}: {self.name}"
    def get_region(self):
        return "+".join(sorted(self.regions))

class XenobladeXLocation(Location):
    game: str = "XenobladeX"

locTypes:list[GroupType] = []

def _generateLocations(prefix:str, type:int, data:list[LocData]) -> Generator[Loc, None, None]:
    offset = locTypes[-1].offset + locTypes[-1].length if locTypes else 0
    locTypes.append(GroupType(prefix, type, offset, len(data)))
    return (Loc(prefix, e.name, type, offset + i + 1, e.regions, e.count) for i, e in enumerate(data) if e.valid)

xenobladeXLocations = [
    *_generateLocations("CLP", 0, collepedia_data),
    *_generateLocations("EBK", 1, enemies_data),
    *_generateLocations("FNO", 2, fn_nodes_data),
    *_generateLocations("SEG", 3, segments_data),
    *_generateLocations("LOC", 4, locations_data),
]

additionalLocNames = [
    "EBK: Lao",
]

def create_location(world:MultiWorld, region_name:str, location_name:str, player:int, abs_id:Optional[int]):
    init_region(world, player, region_name)
    return add_region_location(world, player, region_name, XenobladeXLocation(player, 
        location_name, abs_id, world.get_region(region_name, player)))

def create_locations(world:MultiWorld, player:int, base_id:int, location_name_to_id):
    for location_name in additionalLocNames:
        region = next(location.get_region() for location in xenobladeXLocations if location.get_location() == location_name)
        create_location(world, region, location_name, player, location_name_to_id[location_name])
    for location in xenobladeXLocations:
        if hasattr(world, location.prefix) and not getattr(world, location.prefix)[player].value: continue
        create_location(world, location.get_region(), location.get_location(), player, base_id + location.id)
