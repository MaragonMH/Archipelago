from typing import TYPE_CHECKING
from BaseClasses import CollectionState
from Options import OptionError

if TYPE_CHECKING:
    from . import XenobladeXWorld


def local_fill(world: "XenobladeXWorld") -> None:
    """Place the local only percentage of the items inside its own world"""
    localFillCount = len(world.local_fill_items)
    if localFillCount <= 0:
        return

    minOpenLocations = 3
    localLocations = world.multiworld.get_unfilled_locations(world.player)
    # Probably a useless check, because during generation is fills up the items to the locations
    if len(localLocations) - minOpenLocations < localFillCount:
        raise OptionError(f"Xenoblade X: Not enough locations for local_fill option for {world.player_name}.")

    # Place all the local items without blocking all early locations
    world.random.shuffle(localLocations)
    sphereOneLocs = world.multiworld.get_reachable_locations(CollectionState(world.multiworld), world.player)
    for fillerItem in world.local_fill_items:
        while True:
            loc = localLocations.pop()
            if loc in sphereOneLocs:
                if len(sphereOneLocs) <= minOpenLocations:
                    continue
                sphereOneLocs.remove(loc)
            try:
                loc.place_locked_item(fillerItem)
            except Exception:
                exceptionWorld = loc.item.game if loc.item is not None else "Unknown"
                raise Exception("Xenoblade X: Could not fulfill local_fill option. This issue is caused by another "
                                "world filling Xenoblade X locations during pre_fill.\n"
                                "Archipelago does not allow us to place items into the item pool after "
                                "create_items, so we cannot recover from this issue.\n"
                                f"This is likely caused by the following world(s): {exceptionWorld}.\n"
                                f"Please let the world dev(s) for the listed world(s) know that there is an "
                                f"issue there.\n")
            break
