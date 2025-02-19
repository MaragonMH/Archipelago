from typing import List
from ..Regions import Requirement as Req, Rule

# flake8: noqa
# Mamma Mia
shop_mia_regions: List[Rule] = [
Rule("Menu"),
Rule("Shop Mia", {Req("AMR: Combat Bodywear_1"), Req("WPN: Iron Blades_1")}),
]

# The Bodyguard
shop_bodyguard_regions: List[Rule] = [
Rule("Menu"),
Rule("Shop Bodyguard", {Req("WPN: Warrior Assault Rifle_1"), Req("WPN: Iron Sword_1"), Req("WPN: Titanium Shield_1")}),
]

# Cooking Schooled
shop_cooking_regions: List[Rule] = [
Rule("Menu"),
Rule("Shop Cooking Schooled", {Req("WPN: Chrome Sword_1")}),
]

# Lend an Ear
shop_lend_ear_regions: List[Rule] = [
Rule("Menu"),
Rule("Shop Lend an Ear", {Req("WPN: Chrome Knife_1")}),
]

# Boot Camp
shop_boot_camp_regions: List[Rule] = [
Rule("Menu"),
Rule("Shop Boot Camp", {Req("WPN: Soldier Assault Rifle_1")}),
]

shop_regions: List[Rule] = [
    *shop_mia_regions,
    *shop_bodyguard_regions,
    *shop_cooking_regions,
    *shop_lend_ear_regions,
    *shop_boot_camp_regions
]
