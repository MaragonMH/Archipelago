import typing
from collections import OrderedDict
from ..generic.Rules import add_rule
from .Regions import connect_regions

# Requirements to advance to the next region
# Use dict to specify the quantity you need
xenobladeXRegionRules = OrderedDict({
    "Chapter 1": {},
    "Chapter 2": {},
    "Chapter 3": {},
    "Chapter 4": {
        "Data Probe G1": {"count": 3}, 
        "Research Probe G1": {"count": 1}, 
        "Frontier Nav": {}
    },
    "Chapter 5": {},
    "Chapter 6": {},
    "Chapter 7": {},
    "Chapter 8": {"Lao Heart": {"count": 1}},
    "Chapter 9": {},
    "Chapter 10": {},
    "Chapter 11": {"Gwin Heart": {"count": 1}},
    "Chapter 12": {"Skell-License": {}, "Skell-Flight-Module": {}},
    "Epilogue": {}
})

# Specifiy a location and a list of required items
# Use dict for count
# Use Array for or rules
xenobladeXRegionRules = {
    "Segment 1": [{"Frontier Nav"}],
}

def _has_items(state, player, requirements) -> bool:
    result = True
    for locationName, requirement in requirements.items():
        count = requirement["count"] if "count" in requirement else 0
        received = 0
        for idx in range(count):
            appendix = " #" + str(idx) if count > 0 else ""
            if state.has(locationName + appendix, player): 
                received += 1
        if count == 0:
            count += 1
        if received < count:
            return False
    return result


def set_rules(world, player):
    world.completion_condition[player] = lambda state: state.can_reach("Epilogue", 'Location', player)

    for i, (chapter, requirements) in enumerate (xenobladeXRegionRules.items()):
        # Region connection. Only for advancing chapters
        connect_regions(world, player, chapter, xenobladeXRegionRules.items()[i + 1], lambda state: _has_items(state, player, requirements))

    for (location, rules) in xenobladeXRegionRules.items():
        for requirements in rules:
            # Location connection. Further requirements, if the chapter criteria is fullfilled
            add_rule(world.get_location(location, player), lambda state: _has_items(state, player, requirements))
