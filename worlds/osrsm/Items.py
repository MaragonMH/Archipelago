import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemNames


class ItemRow(typing.NamedTuple):
    name: str
    amount: int
    progression: ItemClassification
    cannonical_chunk: str|None


class OSRSMItem(Item):
    game: str = "Old School Runescape Members"
    item_type: typing.ClassVar[str] = "generic"


class OSRSMTrainingItem(OSRSMItem):
    item_type = "training"
    skill_name: str
    skill_level: int
    pseudo_item_name: str

    def __init__(self, skill_name: str, skill_level: int, player: int):
        name = f"Training_{skill_name}_{skill_level}"
        super().__init__(name, ItemClassification.progression, None, player)
        self.skill_name = skill_name
        self.skill_level = skill_level
        self.pseudo_item_name = "_Max_Training_" + skill_name


class OSRSMQuestPointItem(OSRSMItem):
    item_type = "quest_point"
    quest_point_reward: int

    def __init__(self, quest_point_reward: int, location_name: str, player: int):
        name = f"QP {quest_point_reward} ({location_name})"
        super().__init__(name, ItemClassification.progression, None, player)
        self.quest_point_reward = quest_point_reward


class OSRSMKudosItem(OSRSMItem):
    item_type = "kudos"
    kudos_reward: int

    def __init__(self, kudos_reward: int, location_name: str, player: int):
        name = f"Kudos {kudos_reward} ({location_name})"
        super().__init__(name, ItemClassification.progression, None, player)
        self.kudos_reward = kudos_reward


class OSRSMCombatPointsItem(OSRSMItem):
    item_type = "combat_points"
    combat_point_reward: int

    def __init__(self, combat_point_reward: int, location_name: str, player: int):
        name = f"CombatPoints {combat_point_reward} ({location_name})"
        super().__init__(name, ItemClassification.progression, None, player)
        self.combat_point_reward = combat_point_reward


QP_Items: typing.List[str] = [
    ItemNames.QP_Cooks_Assistant,
    ItemNames.QP_Demon_Slayer,
    ItemNames.QP_Restless_Ghost,
    ItemNames.QP_Romeo_Juliet,
    ItemNames.QP_Sheep_Shearer,
    ItemNames.QP_Shield_of_Arrav,
    ItemNames.QP_Ernest_the_Chicken,
    ItemNames.QP_Vampyre_Slayer,
    ItemNames.QP_Imp_Catcher,
    ItemNames.QP_Prince_Ali_Rescue,
    ItemNames.QP_Dorics_Quest,
    ItemNames.QP_Black_Knights_Fortress,
    ItemNames.QP_Witchs_Potion,
    ItemNames.QP_Knights_Sword,
    ItemNames.QP_Goblin_Diplomacy,
    ItemNames.QP_Pirates_Treasure,
    ItemNames.QP_Rune_Mysteries,
    ItemNames.QP_Misthalin_Mystery,
    ItemNames.QP_Corsair_Curse,
    ItemNames.QP_X_Marks_the_Spot,
    ItemNames.QP_Below_Ice_Mountain
]

starting_area_dict: typing.Dict[int, str] = {
    0: ItemNames.Lumbridge,
    1: ItemNames.Al_Kharid,
    2: ItemNames.Central_Varrock,
    3: ItemNames.West_Varrock,
    4: ItemNames.Edgeville,
    5: ItemNames.Falador,
    6: ItemNames.Draynor_Village,
    7: ItemNames.Wilderness,
}

chunksanity_starting_chunks: typing.List[str] = [
    ItemNames.Lumbridge,
    ItemNames.Lumbridge_Swamp,
    ItemNames.Lumbridge_Farms,
    ItemNames.HAM_Hideout,
    ItemNames.Draynor_Village,
    ItemNames.Draynor_Manor,
    ItemNames.Wizards_Tower,
    ItemNames.Al_Kharid,
    ItemNames.Citharede_Abbey,
    ItemNames.South_Of_Varrock,
    ItemNames.Central_Varrock,
    ItemNames.Varrock_Palace,
    ItemNames.Lumberyard,
    ItemNames.West_Varrock,
    ItemNames.Edgeville,
    ItemNames.Barbarian_Village,
    ItemNames.Monastery,
    ItemNames.Ice_Mountain,
    ItemNames.Dwarven_Mines,
    ItemNames.Falador,
    ItemNames.Falador_Farm,
    ItemNames.Crafting_Guild,
    ItemNames.Rimmington,
    ItemNames.Port_Sarim,
    ItemNames.Mudskipper_Point,
    ItemNames.Wilderness
]

# Some starting areas contain multiple regions, so if that area is rolled for Chunksanity, we need to map it to one
chunksanity_special_region_names: typing.Dict[str, str] = {
    ItemNames.Lumbridge_Farms: 'Lumbridge Farms East',
    ItemNames.Crafting_Guild: 'Crafting Guild Outskirts',
}
