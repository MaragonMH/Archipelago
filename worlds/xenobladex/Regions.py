from typing import TYPE_CHECKING
from BaseClasses import Region, Entrance, Location

if TYPE_CHECKING:
    from . import XenobladeXWorld


def init_region(world: "XenobladeXWorld", region_name: str) -> None:
    """Initialize the new region if it was not done before and establish the connection rules,
        based on its predecessors, if applicable"""
    if region_name not in [reg.name for reg in world.get_regions()]:
        world.multiworld.regions += [Region(region_name, world.player, world.multiworld)]


def add_region_location(world: "XenobladeXWorld", region_name: str, location: Location) -> Location:
    region = world.get_region(region_name)
    region.locations += [location]
    return location


def connect_regions(world: "XenobladeXWorld", source: str, target: str, rule):
    """Connect a single region to another with a specified rule"""
    source_region = world.get_region(source)
    target_region = world.get_region(target)

    connection = Entrance(world.player, target, source_region)
    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
