import logging
from BaseClasses import MultiWorld, Region, Entrance, RegionType, Location
from .regions.key import doll_regions, fnet_regions
from .regions.chapters import chapter_regions
from .regions.friends import friends_nagi_regions, friends_l_regions, friends_lao_regions, friends_gwin_regions, friends_frye_regions, \
    friends_doug_regions, friends_phog_regions, friends_elma_regions, friends_lin_regions, friends_celica_regions, \
    friends_irina_regions, friends_murderess_regions, friends_hope_regions, friends_mia_regions
from .regions.fieldSkills import mechanical_regions, biological_regions, archeological_regions

xenobladeXRegions = { rule.region for rule in [
    *chapter_regions,
    *friends_nagi_regions,
    *friends_l_regions,
    *friends_lao_regions,
    *friends_gwin_regions,
    *friends_frye_regions,
    *friends_doug_regions,
    *friends_phog_regions,
    *friends_elma_regions,
    *friends_lin_regions,
    *friends_celica_regions,
    *friends_irina_regions,
    *friends_murderess_regions,
    *friends_hope_regions,
    *friends_mia_regions,
    *doll_regions,
    *fnet_regions,
    *mechanical_regions,
    *biological_regions,
    *archeological_regions,
]}

def init_region(world: MultiWorld, player: int, region_name:str):
    if region_name not in [region.name for region in world.regions] and set(region_name.split("+")) <= xenobladeXRegions:
        logging.info(f"Region Name: {region_name}")
        world.regions += [Region(region_name, RegionType.Generic, region_name, player, world)]


def add_region_location(world: MultiWorld, player: int, region_name: str, location:Location):
    region = world.get_region(region_name, player)
    region.locations += [location]


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    """Connect a single region to another with a specified rule"""
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    connection = Entrance(player,'', source_region)
    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
