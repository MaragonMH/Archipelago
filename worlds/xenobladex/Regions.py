import logging
from functools import partial
from BaseClasses import CollectionState, MultiWorld, Region, Entrance, EntranceType, Location
from dataclasses import astuple, dataclass, field


@dataclass(frozen=True, eq=True)
class Requirement:
    name: str
    count: int = 1


@dataclass(frozen=True)
class Rule:
    region: str
    requirements: set[Requirement] = field(default_factory=lambda: set())


@dataclass(frozen=True)
class Miranium:
    st: int = 0
    dp: int = 0
    b1: int = 0
    b2: int = 0
    mech: int = 1


@dataclass(frozen=True)
class Credits:
    r1: int = 0
    r2: int = 0
    r3: int = 0
    r4: int = 0
    r5: int = 0
    r6: int = 0
    dp: int = 0
    b1: int = 0
    b2: int = 0
    mech: int = 1


from .regions.chapters import chapter_regions  # noqa: E402
from .regions.fieldSkills import field_skill_regions  # noqa: E402
from .regions.fnet import fnet_regions  # noqa: E402
from .regions.friends import friends_regions  # noqa: E402
from .regions.key import key_regions  # noqa: E402
from .regions.shop import shop_regions  # noqa: E402
from .regions.zones import zones_regions  # noqa: E402
from .fnet.miranium import fnet_miranium_data  # noqa: E402
from .fnet.credits import fnet_credits_data  # noqa: E402

xenobladeXRegions = [
    *chapter_regions,
    *field_skill_regions,
    *fnet_regions,
    *friends_regions,
    *key_regions,
    *shop_regions,
    *zones_regions
]


def init_region(world: MultiWorld, player: int, region_name: str):
    """Initialize the new region if it was not done before and establish the connection rules,
        based on its predecessors, if applicable"""
    region_names = [region.name for region in world.get_regions(player)]
    regions = set([rule.region for rule in xenobladeXRegions])
    if region_name not in region_names and set(region_name.split("+")) <= regions:
        logging.debug(f"Region Name: {region_name}")
        world.regions += [Region(region_name, player, world, region_name)]
        if region_name == "Menu":
            return

        # Add connections to this region
        requirements: set[Requirement] = set()
        for subregion in region_name.split("+"):
            region_found = False
            for rule in reversed(xenobladeXRegions):
                if rule.region != subregion and not region_found:
                    continue
                region_found = True
                if rule.region == "Menu":
                    break
                requirements = requirements.union(rule.requirements)
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

    connection = Entrance(player, target, source_region, randomization_type=EntranceType.TWO_WAY)
    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)


def has_items(state: CollectionState, player, requirements: set[Requirement]) -> bool:
    """Returns true if the state satifies the item requirements"""
    result = True
    for requirement in requirements:
        if requirement.name == "MIRANIUM":
            result = result and has_miranium(state, player, requirement.count)
        elif requirement.name == "CREDITS":
            result = result and has_credits(state, player, requirement.count)
        elif requirement.name in state.multiworld.worlds[player].item_name_groups:
            result = result and state.has_group(requirement.name, player)
        elif requirement.name in ["MIRA", "PRIM", "NOCT", "OBLI", "SYLV", "CAUL"]:
            zone_segment_count = 0
            for loc in state.multiworld.get_reachable_locations(state, player):
                if loc.name.startswith(("SEG", "FNO")):
                    if requirement.name == "MIRA":
                        zone_segment_count += 1
                    elif f"- {requirement.name.capitalize()}" in loc.name:
                        zone_segment_count += 1
            result = result and zone_segment_count >= requirement.count
        else:
            result = result and state.has(requirement.name, player, requirement.count)
    return result


def has_miranium(state: CollectionState, player, target: int) -> bool:
    st = state.count("DP: Storage Probe", player)
    dp = state.count("DP: Duplicator Probe", player)
    b1 = state.count("DP: Booster Probe G1", player)
    b2 = state.count("DP: Booster Probe G2", player)
    mech = state.count("FLDSK: Mechanical", player) + 1
    mir_state = Miranium(st, dp, b1, b2, mech)
    miranium = 6  # fnet default
    for value, mirs in fnet_miranium_data.items():
        for mir in mirs:
            possible = True
            for it1, it2 in zip(astuple(mir), astuple(mir_state)):
                possible = possible and it1 <= it2
            if possible:
                miranium = value
    return miranium >= target


def has_credits(state: CollectionState, player, target) -> bool:
    r = [state.count(f"DP: Research Probe G{i}", player) for i in range(1, 7)]
    dp = state.count("DP: Duplicator Probe", player)
    b1 = state.count("DP: Booster Probe G1", player)
    b2 = state.count("DP: Booster Probe G2", player)
    mech = state.count("FLDSK: Mechanical", player) + 1
    crd_state = Credits(r[0], r[1], r[2], r[3], r[4], r[5], dp, b1, b2, mech)
    credits = 0
    for value, crds in fnet_credits_data.items():
        for crd in crds:
            possible = True
            for it1, it2 in zip(astuple(crd), astuple(crd_state)):
                possible = possible and it1 <= it2
            if possible:
                credits = value
    return credits >= target
