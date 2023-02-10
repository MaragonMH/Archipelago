import typing
from BaseClasses import MultiWorld, Region, Entrance, Location, RegionType
from .Locations import XenobladeXLocation

# specifiy all the locations inside a region
xenobladeXRegions = {
    "Menu" : {},
    "Chapter 1": {"Segment 1"},
    "Chapter 2": {},
    "Chapter 3": {},
    "Chapter 4": {},
    "Chapter 5": {},
    "Chapter 6": {},
    "Chapter 7": {},
    "Chapter 8": {},
    "Chapter 9": {},
    "Chapter 10": {},
    "Chapter 11": {},
    "Chapter 12": {},
    "Epilogue": {},
}

def create_regions(world: MultiWorld, player: int, location_name_to_id):
    for chapter in xenobladeXRegions:
        region = Region(chapter, RegionType.Generic, chapter, player, world)
        region.locations += [XenobladeXLocation(player, location_name, location_name_to_id[location_name], region) for location_name in xenobladeXRegions[chapter]]
        world.regions.append(region)


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player,'', sourceRegion)
    connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)