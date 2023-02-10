from Options import Option, DeathLink, Toggle, DefaultOnToggle, Choice

class NamedChoice(Choice):
    cemu_selection_names: list[str] = []

class EnemyAggro(NamedChoice):
    """Increase or decrease the enemy aggression"""
    display_name = "Enemy Aggro"
    option_none = 0
    option_hell_never_deaggro = 1
    option_increase_range_x2 = 2
    option_decrease_range_2 = 3
    option_decrease_range_4 = 4
    cemu_selection_names = [
        "off",
        "Hell: Enemies will never de-aggro",
        "Increase Range x2",
        "Decrease Range / 2",
        "Decrease Range / 4",
    ]



class EnemyStats(NamedChoice):
    """Adjust the stats of the enemies"""
    display_name = "Damage Divisor"
    option_none = 0
    option_25_percent = 1
    option_50_percent = 2
    option_75_percent = 3
    option_125_percent = 4
    option_150_percent = 5
    option_200_percent = 6
    option_hell_300_percent = 7
    option_impossible_1000_percent = 8
    cemu_selection_names = [
        "off",
        "Set at 25%",
        "Set at 50%",
        "Set at 75%",
        "Set at 125%",
        "Set at 150%",
        "Set at 200%",
        "Hell: Set at 300%",
        "Impossible: Set at 1000%",
    ]


class DamageDivisor(NamedChoice):
    """Divide your teams damage output. Note: Displayed damage values stay the same regardless"""
    display_name = "Damage Divisor"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    cemu_selection_names = [
        "off",
        "Damage / 2",
        "Damage / 3",
        "Damage / 5",
        "Damage / 10",
        "Damage / 50",
        "Damage / 100",
    ]


class DamageMultiplicator(NamedChoice):
    """Multiply your teams damage output. Note: Displayed damage values stay the same regardless"""
    display_name = "Damage Multiplier"
    option_none = 0
    option_x2 = 1
    option_x3 = 2
    option_x5 = 3
    option_x10 = 4
    option_x25 = 5
    option_x100 = 6
    cemu_selection_names = [
        "off",
        "Damage x2",
        "Damage x3",
        "Damage x5",
        "Damage x10",
        "Damage x25",
        "Damage x100",
    ]

class QteAuto(NamedChoice):
    """Automatically completes Quicktime-Events with the specified rating"""
    display_name = "Quicktime-Event Auto"
    option_none = 0
    option_excellent = 1
    option_good = 2
    option_fail = 3
    cemu_selection_names = [
        "off",
        "Force Excellent",
        "Force Good",
        "Force Fail / Disable Soul Voices",
    ]


class QteSpeed(NamedChoice):
    """Sets the speed for every Quicktime-Event manually"""
    display_name = "Quicktime-Event Speed"
    option_none = 0
    option_slow = 1
    option_mid = 2
    option_fast = 3
    option_faster = 4
    cemu_selection_names = [
        "off",
        "Slow",
        "Mid",
        "Fast",
        "Faster",
    ]


class QteSkell(Toggle):
    """Restores skells automatically if the insurance is still valid"""
    display_name = "Skell Recovery"


class CollectionRange(NamedChoice):
    """Increases the collection range of items in the field"""
    display_name = "Collection Range"
    option_none = 0
    option_big = 1
    option_bigger = 2
    cemu_selection_names = [
        "off",
        "Big Range",
        "Bigger Range",
    ]


class ArmorSlotUpgrades(Toggle):
    """Allows you to further upgrade armor slots."""
    display_name = "Armor Slot Upgrades"


class ArmorTraitsUpgrades(NamedChoice):
    """Allows you to further upgrade equipment traits. Optional without ressources"""
    display_name = "Equip Trait Upgrades"
    option_none = 0
    option_normal = 1
    option_cheat = 2
    cemu_selection_names = [
        "off",
        "Normal",
        "CHEAT - Ignore Miranium and resources requirements",
    ]


class LvPointsModifier(NamedChoice):
    """Modifies the level experience gain and disables 9999 exp cap"""
    display_name = "Lv-Points Modifier"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    option_5 = 4
    option_10 = 5
    option_50 = 6
    option_100 = 7
    option_1000 = 8
    cemu_selection_names = [
        "off",
        "x1",
        "x2",
        "x3",
        "x5",
        "x10",
        "x50",
        "x100",
        "x1000",
    ]


class BattlePointsModifier(NamedChoice):
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
    cemu_selection_names = [
        "off",
        "Quantity x2",
        "Quantity x3",
        "Quantity x5",
        "Quantity x10",
        "Quantity x50",
        "Quantity x100",
        "Quantity x1000",
    ]


class BladePointsModifier(NamedChoice):
    """Modifies the BLADE experience gain"""
    display_name = "BLADE-Points Modifier"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    cemu_selection_names = [
        "off",
        "x2",
        "x3",
        "x5",
        "x10",
        "x50",
    ]


class FrontierNavMiraniumFrequency(NamedChoice):
    """Alters the frequency of the Frontier-Nav Miranium bonuses"""
    display_name = "Froniter-Nav Miranium Frequency"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_5 = 3
    option_10 = 4
    option_15 = 5
    option_20 = 6
    cemu_selection_names = [
        "off",
        "Every minute",
        "Every 2 minutes",
        "Every 5 minutes",
        "Every 10 minutes",
        "Every 15 minutes",
        "Every 20 minutes",
    ]


class FrontierNavMiraniumQuantity(NamedChoice):
    """Alters the quantity of the Frontier-Nav Miranium bonuses"""
    display_name = "Froniter-Nav Miranium Quantity"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    cemu_selection_names = [
        "Miranium x1",
        "Miranium x2",
        "Miranium x3",
        "Miranium x5",
        "Miranium x10",
        "Miranium x50",
        "Miranium x100",
    ]


class FrontierNavMoneyFrequency(NamedChoice):
    """Alters the frequency of the Frontier-Nav Money bonuses"""
    display_name = "Froniter-Nav Miranium Frequency"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_5 = 3
    option_7 = 4
    option_10 = 5
    cemu_selection_names = [
        "off",
        "Every minute",
        "Every 2 minutes",
        "Every 5 minutes",
        "Every 7 minutes",
        "Every 10 minutes",
    ]

class FrontierNavMoneyQuantity(NamedChoice):
    """Alters the quantity of the Frontier-Nav Money bonuses"""
    display_name = "Froniter-Nav Miranium Quantity"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    option_1000 = 7
    cemu_selection_names = [
        "off",
        "x2",
        "x3",
        "x5",
        "x10",
        "x50",
        "x100",
        "x1000",
    ]

class FrontierNavResourcesFrequency(NamedChoice):
    """Alters the frequency of the Frontier-Nav Resource bonuses"""
    display_name = "Froniter-Nav Miranium Frequency"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_5 = 3
    cemu_selection_names = [
        "off",
        "Every 1 minute",
        "Every 2 minutes",
        "Every 5 minutes",
    ]


class FrontierNavResourcesQuantity(NamedChoice):
    """Alters the quantity of the Frontier-Nav Resource bonuses"""
    display_name = "Froniter-Nav Miranium Quantity"
    option_none = 0
    option_2 = 1
    option_3 = 2
    option_5 = 3
    option_10 = 4
    option_50 = 5
    option_100 = 6
    cemu_selection_names = [
        "off",
        "x2",
        "x3",
        "x5",
        "x10",
        "x50",
        "x100",
    ]


class FrontierNavNoMiraniumCap(NamedChoice):
    """Removes the Miranium cap caused by missing storage probes"""
    display_name = "Frontier-Nav no Miranium Cap"
    option_off = 0
    option_on = 1
    cemu_selection_names = [
        "Yes",
        "No",
    ]


class EManualChangeTime(Toggle):
    """The E-Manual allows you to change the time from your menu"""
    display_name = "E-Manual Change Time"


class EquipAlternateRatio(Toggle):
    """In vanilla, equipment traits have a percent chance to be selected, some of them have 90 or 100%
    , while others have 10%. This mod changes that: everything above 80% is capped at 80%
    , and everything else is set to 20%"""
    display_name = "Treasure Alternate Ratio"


class EquipChestCount(NamedChoice):
    """Alters the guranteed item count in treasure chests"""
    display_name = "Treasure Chest Count"
    option_none = 0
    option_1 = 1
    option_2 = 2
    option_3 = 3
    cemu_selection_names = [
        "off",
        "Always 1 equipments",
        "Always 2 equipments",
        "Always 3 equipments",
    ]


class EquipQuality(NamedChoice):
    """Alters the guranteed equipment trait count"""
    display_name = "Treasure Traits"
    option_none = 0
    option_0_traits = 1
    option_1_traits = 2
    option_2_traits = 3
    option_3_traits = 4
    cemu_selection_names = [
        "off",
        "Common (0 traits)",
        "Rare (1 trait)",
        "Unique (2 traits)",
        "Prime (3 traits)",
    ]


class EquipSlots(NamedChoice):
    """Alters the guranteed equipment augments slots count"""
    display_name = "Augment Slots"
    option_none = 0
    option_0 = 1
    option_1 = 2
    option_2 = 3
    option_3 = 4
    cemu_selection_names = [
        "off",
        "0 Slots",
        "1 Slot",
        "2 Slots",
        "3 Slots",
    ]


class BrokenEquip(NamedChoice):
    """Alters chance to get broken equipment"""
    display_name = "Broken Treasure"
    option_none = 0
    option_never = 1
    option_always = 2
    cemu_selection_names = [
        "off",
        "Never get broken equipment",
        "Always get broken equipment",
    ]


class MaterialsDropRatio(NamedChoice):
    """Alters the materials drop ratio"""
    display_name = "Treasure Drop Ratio"
    option_none = 0
    option_drop_100_percent = 1
    option_drop_70_percent = 2
    option_drop_50_percent = 3
    option_drop_30_percent = 4
    option_drop_0_percent = 5
    cemu_selection_names = [
        "off",
        "Set minimum drop to 100% (always drop)",
        "Set minimum drop to 70% (always drop)",
        "Set minimum drop to 50% (always drop)",
        "Set minimum drop to 30% (always drop)",
        "Set minimum drop to 0% (never drop)",
    ]


class TreasureQuality(NamedChoice):
    """Forces a specific quality"""
    display_name = "Treasure Quality"
    option_none = 0
    option_gold_quality = 1
    option_silver_quality = 2
    option_bronze_quality = 3
    option_no_treasure = 4
    cemu_selection_names = [
        "off",
        "Gold quality",
        "Silver quality",
        "Bronze quality",
        "No treasure",
    ]


class MoonJumpWidth(NamedChoice):
    """Alters the jump width"""
    display_name = "Moon Jump Width"
    option_none = 0
    option_distance_150_percent = 1
    option_distance_160_percent = 2
    option_distance_170_percent = 3
    option_distance_180_percent = 4
    option_distance_190_percent = 5
    option_distance_200_percent = 6
    option_distance_250_percent = 7
    option_distance_300_percent = 8
    option_distance_500_percent = 9
    option_cheat_1000_percent = 10
    cemu_selection_names = [
        "Distance x1.0 (default)",
        "Distance x1.5",
        "Distance x1.6",
        "Distance x1.7",
        "Distance x1.8",
        "Distance x1.9",
        "Distance x2.0",
        "Distance x2.5",
        "Distance x3.0",
        "Distance x5.0",
        "CHEAT x100.0",
    ]


class MoonJumpHeight(NamedChoice):
    """Alters the jump height"""
    display_name = "Moon Jump Height"
    option_none = 0
    option_height_105_percent = 1
    option_height_106_percent = 2
    option_height_107_percent = 3
    option_height_108_percent = 4
    option_height_109_percent = 5
    option_height_110_percent = 6
    option_height_120_percent = 7
    option_height_130_percent = 8
    option_height_140_percent = 9
    option_height_150_percent = 10
    option_height_2500_percent = 11
    cemu_selection_names = [
        "Height x1.0 (default)",
        "Height x1.05",
        "Height x1.06",
        "Height x1.07",
        "Height x1.08",
        "Height x1.09",
        "Height x1.10",
        "Height x1.20",
        "Height x1.30",
        "Height x1.40",
        "Height x1.50",
        "CHEAT x25.0",
    ]


class MoonJumpType(NamedChoice):
    """Alters the landing type after the jump"""
    display_name = "Moon Jump Type"
    option_short_land = 0
    option_step_forward = 1
    option_normal_land = 2
    option_role = 3
    option_full_stop = 4
    option_half_stop = 5
    option_never_land_softlocks = 6
    cemu_selection_names = [
        "Short land (4)",
        "Step foreward (6)",
        "Normal land (5)",
        "Role (3)",
        "Full stop (2)",
        "Half stop (1)",
        "Never land (0) SOFT LOCKS",
    ]


class RunForrestRun(NamedChoice):
    """Alters the running speed"""
    display_name = "Run Forrest, Run"
    option_none = 0
    option_speed_125_percent = 1
    option_speed_150_percent = 2
    option_speed_200_percent = 3
    option_speed_300_percent = 4
    option_cheat_2000_percent = 5
    cemu_selection_names = [
        "off",
        "Speed x1.25",
        "Speed x1.5",
        "Speed x2",
        "Speed x3",
        "CHEAT x20",
    ]


class WeatherForce(Toggle):
    """Allows you to force a weather condition. This option needs to be invoked manually through the graphic packs"""
    display_name = "Force Weather"

# currently unused
class SkellWeaponFamily(DefaultOnToggle):
    """There is only one check for each Skell-Weapon. If enabled, you will receive ALL Weapon tiers (20, 30, 40, 50, 60)
     and rarity (_, X, XX), when you receive the item. If disabled, you will receive one Weapon tier and rarity,
     choosen at random."""
    display_name = "Receive Entire Skell-Weapon-Family"

# currently unused
class AugmentFamily(DefaultOnToggle):
    """There is only one check for each Augment. If enabled, you will receive ALL Augment tiers (I, V, X, XV, XX),
     when you receive the item. If disabled, you will receive one Augment tier, choosen at random."""
    display_name = "Receive Entire Augment-Family"

class IncludeCollectopediaLocations(DefaultOnToggle):
    """Allows you to get items from collectopedia entries and adds those locations to the pool"""
    display_name = "Include Collectopedia Locations"

class IncludeEnemyBookLocations(DefaultOnToggle):
    """Allows you to get items from completing enemy entries(white dot in the menu) and adds those locations to the pool"""
    display_name = "Include Enemy Book Locations"

class IncludeLocationLocations(DefaultOnToggle):
    """Allows you to get items from locations and adds those locations to the pool"""
    display_name = "Include Location Locations"

class IncludeGroundArmor(DefaultOnToggle):
    """Allows you to receive ground armor as items and adds those items to the pool"""
    display_name = "Include Ground Armor Items"

class IncludeGroundWeapons(DefaultOnToggle):
    """Allows you to receive ground weapons as items and adds those items to the pool"""
    display_name = "Include Ground Weapon Items"

class IncludeGroundAugments(DefaultOnToggle):
    """Allows you to receive ground augments as items and adds those items to the pool"""
    display_name = "Include Ground Augment Items"

class IncludeSkellArmor(DefaultOnToggle):
    """Allows you to receive skell armor as items and adds those items to the pool"""
    display_name = "Include Skell Armor Items"

class IncludeSkellWeapons(DefaultOnToggle):
    """Allows you to receive skell weapons as items and adds those items to the pool"""
    display_name = "Include Skell Weapons Items"

class IncludeSkellAugments(DefaultOnToggle):
    """Allows you to receive skell augments as items and adds those items to the pool"""
    display_name = "Include Skell Augment Items"

class LogicCheating(Toggle):
    """Allows you to get the randomized items the regular way."""
    display_name = "Logic Cheating"


mod_options:dict[str, type[Option]] = {
    "BattleEscapeDistance/Active preset": EnemyAggro,
    "BattleEnemyStats/Active preset": EnemyStats,
    "BattleDamageModGround2/Damage Divisor": DamageDivisor,
    "BattleDamageModGround/Active preset": DamageMultiplicator,
    "BattleQteSoulVoices/Active preset": QteAuto,
    "BattleQteSpeed/Active preset": QteSpeed,
    "BattleQteDollLost/": QteSkell,
    "CollectiblesCatchRange/Active preset": CollectionRange,
    "EquipmentArmorsCanHave3AugmentSlots/": ArmorSlotUpgrades,
    "EquipmentUnlimitedAugmentUpgrades/Active preset": ArmorTraitsUpgrades,
    "ExpInnerExpPointsX/Active preset": LvPointsModifier,
    "ExpBattlePointsX/Active preset": BattlePointsModifier,
    "ExpBladePointsS/Active preset": BladePointsModifier,
    "FrontierNavProbeMiraniumFrequency/Active preset": FrontierNavMiraniumFrequency,
    "FrontierNavProbeMiraniumQuantity/Miranium quantity": FrontierNavMiraniumQuantity,
    "FrontierNavProbeMoneyFrequency/Active preset": FrontierNavMoneyFrequency,
    "FrontierNavProbeMoneyQuantity/Active preset": FrontierNavMoneyQuantity,
    "FrontierNavProbeResourcesFrequency/Active preset": FrontierNavResourcesFrequency,
    "FrontierNavProbeResourcesQuantity/Active preset": FrontierNavResourcesQuantity,
    "FrontierNavProbeMiraniumQuantity/Capped by Storage Probes": FrontierNavNoMiraniumCap,
    "HudChangeTimeFromEmanual/": EManualChangeTime,
    "LootEquipmentsAlternateRandomAffix/": EquipAlternateRatio,
    "LootEquipmentsForceCount/Active preset": EquipChestCount,
    "LootEquipmentsForceQuality/Quality": EquipQuality,
    "LootEquipmentsForceQuality/Number of Slots": EquipSlots,
    "LootEquipmentsIgnoreBroken/Active preset": BrokenEquip,
    "LootMaterialsDrop/Active preset": MaterialsDropRatio,
    "LootTreasureQuality/Active preset": TreasureQuality,
    "PhysicsJumpToTheMoon/Horizontal Velocity (distance reached)": MoonJumpWidth,
    "PhysicsJumpToTheMoon/Vertical Velocity (height)": MoonJumpHeight,
    "PhysicsJumpToTheMoon/Landing type": MoonJumpType,
    "PhysicsRunForrestRun/Active preset": RunForrestRun,
}

xenobladeX_options: dict[str, type[Option]] = {
    **mod_options,
    "CLP": IncludeCollectopediaLocations,
    "EBK": IncludeEnemyBookLocations,
    "LOC": IncludeLocationLocations,
    "AMR": IncludeGroundArmor,
    "WPN": IncludeGroundWeapons,
    "AUG": IncludeGroundAugments,
    "SKWPN": IncludeSkellWeapons,
    "SKAMR": IncludeSkellArmor,
    "SKAUG": IncludeSkellAugments,
    "logic_cheating": LogicCheating,
    "death_link": DeathLink,
    "force_weather": WeatherForce,
}
