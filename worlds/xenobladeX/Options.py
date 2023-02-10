import typing
from Options import Option, DeathLink, Toggle, DefaultOnToggle, Choice


class CollectionRange(Choice):
    """Increases the collection range of items in the field"""
    display_name = "Collection Range"
    option_none = 0
    option_big = 1
    option_bigger = 2


class ArmorSlotUpgrades(Choice):
    """Allows you to further upgrade armor slots. Optional without ressources"""
    display_name = "Armor Slot Upgrades"
    option_none = 0
    option_3 = 1
    option_unlimited = 2
    option_cheat = 3


class LvPointsModifier(Choice):
    """Modifies the level experience gain"""
    display_name = "Lv-Points Modifier"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    option_1000 = 7


class BattlePointsModifier(Choice):
    """Modifies the battle experience gain"""
    display_name = "Battle-Points Modifier"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    option_1000 = 7


class BladePointsModifier(Choice):
    """Modifies the BLADE experience gain"""
    display_name = "BLADE-Points Modifier"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    option_1000 = 7


class FrontierNavFrequency(Choice):
    """Alters the frequency of the Frontier-Nav bonuses"""
    display_name = "Froniter-Nav Frequency"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_5 = 3
    option_10 = 4
    option_15 = 5
    option_20 = 6


class FrontierNavQuantity(Choice):
    """Alters the quantity of the Frontier-Nav bonuses"""
    display_name = "Froniter-Nav Quantity"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6


class FrontierNavNoMiraniumCap(Toggle):
    """Removes the Miranium cap caused by missing storage probes"""
    display_name = "Frontier-Nav no Miranium Cap"


class EManualChangeTime(Toggle):
    """The E-Manual allows you to change the time from your menu"""
    display_name = "E-Manual Change Time"


class TreasureAlternateRatio(Toggle):
    """In vanilla, equipment traits have a percent chance to be selected, some of them have 90 or 100%
    , while others have 10%. This mod changes that: everything above 80% is capped at 80%
    , and everything else is set to 20%"""
    display_name = "Treasure Alternate Ratio"


class TreasureChestCount(Choice):
    """Alters the guranteed treasure chest count"""
    display_name = "Treasure Chest Count"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3


class TreasureTraits(Choice):
    """Alters the guranteed treasure trait count"""
    display_name = "Treasure Traits"
    option_none = 0
    option_0 = 1
    option_1 = 2
    option_2 = 3
    option_3 = 4


class TreasureSlots(Choice):
    """Alters the guranteed treasure augments slots count"""
    display_name = "Augment Slots"
    option_none = 0
    option_0 = 1
    option_1 = 2
    option_2 = 3
    option_3 = 4


class TreasureType(Choice):
    """Alters the treasure type"""
    display_name = "Treasure Type"
    option_none = 0
    option_ground_weapon = 1
    option_ground_armor = 2
    option_skell_armor = 3


class BrokenTreasure(Choice):
    """Alters chance to get broken equipment"""
    display_name = "Broken Treasure"
    option_none = 0
    option_never = 1
    option_always = 2


class TreasureDropRatio(Choice):
    """Alters the treasure drop ratio"""
    display_name = "Treasure Drop Ratio"
    option_none = 0
    option_drop_100 = 1
    option_drop_70 = 2
    option_drop_50 = 3
    option_drop_30 = 4
    option_drop_0 = 5


class TreasureQuality(Choice):
    """Forces a specific quality"""
    display_name = "Treasure Quality"
    option_none = 0
    option_gold_quality = 1
    option_silver_quality = 2
    option_bronze_quality = 3
    option_no_treasure = 4


class MoonJumpWidth(Choice):
    """Alters the jump width"""
    display_name = "Moon Jump Width"
    option_none = 0
    option_distance_x1_5 = 1
    option_distance_x1_6 = 2
    option_distance_x1_7 = 3
    option_distance_x1_8 = 4
    option_distance_x1_9 = 5
    option_distance_x2_0 = 6
    option_distance_x2_5 = 7
    option_distance_x3_0 = 8
    option_distance_x5_0 = 9
    option_cheat_x100_0 = 10


class MoonJumpHeight(Choice):
    """Alters the jump height"""
    display_name = "Moon Jump Height"
    option_none = 0
    option_height_x1_05 = 1
    option_height_x1_06 = 2
    option_height_x1_07 = 3
    option_height_x1_08 = 4
    option_height_x1_09 = 5
    option_height_x1_20 = 6
    option_height_x1_30 = 7
    option_height_x1_40 = 8
    option_height_x1_50 = 9
    option_height_x25_0 = 10


class MoonJumpType(Choice):
    """Alters the landing type after the jump"""
    display_name = "Moon Jump Type"
    option_short_land = 0
    option_step_forward = 1
    option_normal_land = 2
    option_role = 3
    option_full_stop = 4
    option_half_stop = 5
    option_never_land_softlocks = 6


class RunForrestRun(Choice):
    """Alters the running speed"""
    display_name = "Run Forrest, Run"
    option_none = 0
    option_speed_x1_25 = 1
    option_speed_x1_5 = 2
    option_speed_x2 = 3
    option_speed_x3 = 4
    option_cheat_x20 = 5


class WeatherForce(Toggle):
    """Allows you to force a weather condition. This option needs to be invoked manually through the graphic packs"""
    display_name = "Force Weather"


class SkellWeaponFamily(DefaultOnToggle):
    """There is only one check for each Skell-Weapon. If enabled, you will receive ALL Weapon tiers (20, 30, 40, 50, 60)
     and rarity (_, X, XX), when you receive the item. If disabled, you will receive one Weapon tier and rarity,
     choosen at random."""
    display_name = "Receive Entire Skell-Weapon-Family"


class AugmentFamily(DefaultOnToggle):
    """There is only one check for each Augment. If enabled, you will receive ALL Augment tiers (I, V, X, XV, XX),
     when you receive the item. If disabled, you will receive one Augment tier, choosen at random."""
    display_name = "Receive Entire Augment-Family"


class LogicCheating(Toggle):
    """Allows you to get the randomized items the regular way."""
    display_name = "Logic Cheating"


xenobladeX_options: typing.Dict[str, type[Option]] = {
    "collection_range": CollectionRange,
    "armor_slot_upgrades": ArmorSlotUpgrades,
    "lv_points_modifier": LvPointsModifier,
    "battle_points_modifier": BattlePointsModifier,
    "blade_points_modifier": BladePointsModifier,
    "frontier_nav_frequency": FrontierNavFrequency,
    "frontier_nav_qualitiy": FrontierNavQuantity,
    "frontier_nav_no_miranium_cap": FrontierNavNoMiraniumCap,
    "e_manual_change_time": EManualChangeTime,
    "treasure_alternate_ratio": TreasureAlternateRatio,
    "treasure_chest_count": TreasureChestCount,
    "treasure_traits": TreasureTraits,
    "treasure_slots": TreasureSlots,
    "treasure_type": TreasureType,
    "broken_treasure": BrokenTreasure,
    "treasure_qualitiy": TreasureQuality,
    "moon_jump_width": MoonJumpWidth,
    "moon_jump_height": MoonJumpHeight,
    "moon_jump_type": MoonJumpType,
    "run_forrest_run": RunForrestRun,
    "weather_force": WeatherForce,
    "skell_weapon_family": SkellWeaponFamily,
    "augment_family": AugmentFamily,
    "logic_cheating": LogicCheating,
    "death_link": DeathLink,
}
