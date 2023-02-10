from BaseClasses import Location, MultiWorld
from .dataType import GroupType
from .locations.collepedia import collepedia_data
from .locations.enemies import enemies_data
from .locations.fnNodes import fn_nodes_data
from .locations.locations import locations_data
from .locations.segments import segments_data
from .Regions import add_region_location, init_region
from typing import NamedTuple

class Loc(NamedTuple):
    prefix: str
    name: str
    type: int
    id: int
    regions: list[str]
    def get_location(self):
        return f"{self.prefix}: {self.name}"


class XenobladeXLocation(Location):
    game: str = "XenobladeX"

locTypes:dict[str, GroupType] = {
    "CLP": GroupType(0),
    "EBK": GroupType(1),
    "FNO": GroupType(2),
    "SEG": GroupType(3),
    "LOC": GroupType(4),
}

xenobladeXLocations = [
    *(Loc(f"CLP", e.name, locTypes["CLP"].type, i + 1, e.regions) for i, e in enumerate(collepedia_data) if e.valid),
    *(Loc(f"EBK", e.name, locTypes["EBK"].type, i + 1, e.regions) for i, e in enumerate(enemies_data) if e.valid),
    *(Loc(f"FNO", e.name, locTypes["FNO"].type, i + 1, e.regions) for i, e in enumerate(fn_nodes_data) if e.valid),
    *(Loc(f"SEG", e.name, locTypes["SEG"].type, i + 1, e.regions) for i, e in enumerate(segments_data) if e.valid),
    *(Loc(f"LOC", e.name, locTypes["LOC"].type, i + 1, e.regions) for i, e in enumerate(locations_data) if e.valid),
]

def calculate_location_type_offsets():
    for prefix, group in locTypes.items():
        group.offset = next(i for i, loc in enumerate(xenobladeXLocations) if loc.prefix == prefix)

def create_locations(world:MultiWorld, player:int):
    for i, location in enumerate(xenobladeXLocations):
        region_name = "+".join(sorted(location.regions))
        init_region(world, player, region_name)
        add_region_location(world, player, region_name, XenobladeXLocation(player, 
            location.get_location(), i, world.get_region(region_name, player)))

def create_location_event(world:MultiWorld, region_name:str, location_name:str, player:int):
    """Create a location event"""
    region = world.get_region(region_name, player)
    location_event = XenobladeXLocation(player, location_name, None, region)
    location_event.event = True
    region.locations += [location_event]
    return location_event
