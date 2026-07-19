from functools import reduce
import operator
from typing import TYPE_CHECKING
from rule_builder.rules import Has, Rule, True_

if TYPE_CHECKING:
    from . import XenobladeXWorld

from .Items import create_item
from .Locations import xenobladeXLocations
from .rules.doll import doll_rules
from .rules.fieldSkills import field_skill_rules
from .rules.fnet import fnet_rules
from .rules.friends import friends_rules
from .rules.importantItems import important_item_rules
from .rules.level import level_rules
from .rules.quests import quest_rules
from .rules.shop import shop_rules
from .rules.zones import zone_rules


xenobladeXRules: dict[str, Rule] = {
    **doll_rules,
    **field_skill_rules,
    **fnet_rules,
    **friends_rules,
    **important_item_rules,
    **level_rules,
    **quest_rules,
    **shop_rules,
    **zone_rules,
}


def set_rules(world):
    """Setting all the rules for region connections and region->item connections"""
    for loc in world.get_locations():
        rule_names = xenobladeXLocations[loc.name].rules
        rules = [xenobladeXRules[rule] for rule in rule_names]
        if not rules:
            rules = [True_()]
        new_rules = reduce(operator.iand, rules)
        print(new_rules)
        world.set_rule(loc, new_rules)

    world.get_location("EBK: Lao Boss - Chp 12: Story").place_locked_item(create_item(world, "KEY: Victory"))

    world.set_completion_rule(Has("KEY: Victory"))
