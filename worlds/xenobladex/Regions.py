import logging
from functools import partial
from collections import OrderedDict
from BaseClasses import CollectionState, MultiWorld, Region, Entrance, Location
from dataclasses import dataclass, field


@dataclass(frozen=True, eq=True)
class Requirement:
    name: str
    count: int = 1


@dataclass(frozen=True)
class Rule:
    region: str
    requirements: set[Requirement] = field(default_factory=lambda: set())


from .regions.key import doll_regions, fnet_regions  # noqa: E402
from .regions.chapters import chapter_regions  # noqa: E402
from .regions.friends import friends_nagi_regions, friends_l_regions, friends_lao_regions, friends_gwin_regions, \
    friends_frye_regions, friends_doug_regions, friends_phog_regions, friends_elma_regions, friends_lin_regions, \
    friends_celica_regions, friends_irina_regions, friends_murderess_regions, \
    friends_hope_regions, friends_mia_regions  # noqa: E402
from .regions.fieldSkills import mechanical_regions, biological_regions, archeological_regions  # noqa: E402

xenobladeXRegions = OrderedDict({rule.region: rule.requirements for rule in [
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
]})


def init_region(world: MultiWorld, player: int, region_name: str):
    """Initialize the new region if it was not done before and establish the connection rules,
        based on its predecessors, if applicable"""
    region_names = [region.name for region in world.get_regions(player)]
    if region_name not in region_names and set(region_name.split("+")) <= set(xenobladeXRegions.keys()):
        logging.debug(f"Region Name: {region_name}")
        world.regions += [Region(region_name, player, world, region_name)]
        if region_name == "Menu":
            return

        # Add connections to this region
        requirements: set[Requirement] = set()
        for subregion in region_name.split("+"):
            region_found = False
            for region, req in reversed(xenobladeXRegions.items()):
                if region != subregion and not region_found:
                    continue
                region_found = True
                if region == "Menu":
                    break
                requirements = requirements.union(req)
        connect_regions(world, player, "Menu", region_name,
                        partial(has_items, player=player, requirements=requirements))


def add_region_location(world: MultiWorld, player: int, region_name: str, location: Location) -> Location:
    region = world.get_region(region_name, player)
    region.locations += [location]
    return location


def connect_regions(world: MultiWorld, player: int, source: str, target: str, rule):
    """Connect a single region to another with a specified rule"""
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    connection = Entrance(player, '', source_region)
    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


def has_items(state: CollectionState, player, requirements: set[Requirement]) -> bool:
    """Returns true if the state satifies the item requirements"""
    result = True
    for requirement in requirements:
        result = result and state.has(requirement.name, player, requirement.count)
    return result
