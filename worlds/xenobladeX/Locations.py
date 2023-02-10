from BaseClasses import Location, MultiWorld
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


class XenobladeXLocation(Location):
    game: str = "XenobladeX"

xenobladeXLocations = [
    *(Loc(f"CLP: ", e.name, 0, i + 1, e.regions) for i, e in enumerate(collepedia_data) if e.valid),
    *(Loc(f"EBK: ", e.name, 1, i + 1, e.regions) for i, e in enumerate(enemies_data) if e.valid),
    *(Loc(f"FNO: ", e.name, 2, i + 1, e.regions) for i, e in enumerate(fn_nodes_data) if e.valid),
    *(Loc(f"SEG: ", e.name, 3, i + 1, e.regions) for i, e in enumerate(segments_data) if e.valid),
    *(Loc(f"LOC: ", e.name, 4, i + 1, e.regions) for i, e in enumerate(locations_data) if e.valid),
]

def create_locations(world:MultiWorld, player:int):
    for i, location in enumerate(xenobladeXLocations):
        region_name = "+".join(sorted(location.regions))
        init_region(world, player, region_name)
        add_region_location(world, player, region_name, XenobladeXLocation(player, 
            location.prefix + location.name, i, world.get_region(region_name, player)))

def create_location_event(world:MultiWorld, region_name:str, location_name:str, player:int):
    """Create a location event"""
    region = world.get_region(region_name, player)
    location_event = XenobladeXLocation(player, location_name, None, region)
    location_event.event = True
    region.locations += [location_event]
    return location_event
