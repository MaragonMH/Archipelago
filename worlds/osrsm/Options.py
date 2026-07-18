from dataclasses import dataclass
from typing import Any, Dict

from Options import Choice, Toggle, DefaultOnToggle, Range, NamedRange, PerGameCommonOptions,FreeText,Visibility,OptionDict,LocationSet,TextChoice, OptionSet
from .LogicCSV.macros_generated2 import skill_names
from .LogicCSV.items_generated2 import rollable_chunks
from schema import Schema,Optional,And

logic_relevent_options = [
    "goal_type","bingo_size","max_drop_rate","full_drop_rate","maximum_training_levels","starting_skill_levels",
    "qp_per_level","levels_per_qp","base_training_levels","tutorial_island_items","pre_completed_tasks","banned_chunks"
]

locations = {"option_" + start: i for i, start in enumerate(rollable_chunks.keys())}
# This way the dynamic start names are picked up by the MetaClass Choice belongs to
StartingArea = type("StartingArea", (TextChoice,), {
    "__module__": __name__,
    "display_name": "Starting Region",
    "default":"Lumbridge Castle",
    "__doc__": """Which chunks are available at the start. The player may need to move through locked chunks to reach the starting
               area, but any areas that require quests, skills, or coins are not available as a starting location
               
               NOTE: MEMBERS LOGIC ISSUE: WE DON'T ACTUALLY CARE ABOUT WHAT YOUR START COULD BE HAVE FUN!""",
    **locations,
})
del (locations)

class GoalType(Choice):
    """
    Decide what kind of goal you want
    Task  : Your goal is a specific task
    Bingo : Your goal is to complete the Bingo board
    Both  : You goal is to complete a specific task AND clear the bingo board
    """
    display_name = "Goal Type"
    option_task  = 0
    option_bingo = 1
    option_both  = 2
    default = 0

class GoalLocation(FreeText):
    """
    Which location name to consider to be the goal.
    """
    display_name = "Goal Location"
    default = "~|Dragon Slayer I|~ Complete the quest"

class BingoSize(Range):
    """
    How Big of a bingo board to generate, value is used for both the width and height
    
    Locations will be sent for every column, row, and diagonal
    """
    display_name = "Bingo Size"
    default = 9
    range_start = 3
    range_end = 51

class DisableChunkCulling(Choice):
    """
    Disable the culling that reduces the number of chunks that are in the "playable" space
    DO NOT DO THIS UNLESS YOU HATE YOURSELF MORE THEN A NORMAL OSRS PLAYER

    Useful will convert the chunks to useful, this means they won't actually be removed just not considered for logic
    """
    display_name = "Disable Chunk Culling"
    option_enabled = 0
    option_useful = 1
    option_disabled = 2
    default = 0
class DisableLocationCulling(Toggle):
    """
    Disable the culling that reduces the number of Tasks that get created
    This might create much smaller spheres, if this becomes a problem I will have to find a way to tone it down more
    """
    display_name = "Disable Task Culling"
    default = False

class MaxDropRate(Range):
    """
    The Maximum drop rate that will be considered logical access
    Be careful as to low a value might make your game unbeatable or at least VERY convoluted
    """
    display_name = "Maximum Drop Rate"
    default = 1024
    range_start = 1
    range_end = 10_000 #uncut onyx from the elven crystal chest

class FullMaxDropRate(Range):
    """
    Override for Maximum Drop Rate that allows for choosing values that are VERY ill advised
    Leave at 0 if you don't know what you're doing
    Use with extreme caution
    """
    dispaly_name = "Full Maximum Drop Rate"
    default = 0
    range_start = 0
    range_end = 100_000_000 #uncut onyx from a gem back
    visibility = Visibility(Visibility.all - Visibility.simple_ui)


class MaxTrainingLevels(OptionDict):
    """
    The maximum levels that you will be expected to train each skill
    """
    display_name = "Maximum Required Skill Levels"
    valid_keys = frozenset(skill_names)
    default = {skill_name:(99 if skill_name != "Combat" else 100) for skill_name in skill_names}
    schema = Schema({
        Optional(skill_name):And(int,lambda n: 100>= n >= 0,error="Skill Level must be integers in the range of 0-99.")
        for skill_name in skill_names
    })

    def __init__(self, value: Dict[str, Any]):
        self.value = {}
        for key,data in value.items():
            try:
                self.value[key] = MaxTrainingLevel.from_any(data).value
            except ValueError:
                self.value[key] = data


class StartingLevels(OptionDict):
    """
    The starting levels that your character has prior to starting the multiworld
    """
    display_name = "Initial Skill Levels"
    valid_keys = frozenset(skill_names)
    default = {skill_name:(0 if skill_name != "Hitpoints" else 10) for skill_name in skill_names}
    schema = Schema({
        Optional(skill_name):And(int,lambda n: 100>= n >= 0,error="Skill Level must be integers in the range of 0-99.")
        for skill_name in skill_names
    })

    def __init__(self, value: Dict[str, Any]):
        self.value = {}
        for key,data in value.items():
            try:
                self.value[key] = MaxTrainingLevel.from_any(data).value
            except ValueError:
                self.value[key] = data

class MaxTrainingLevel(Range):
    default = 99
    range_start = 0
    range_end = 100
    visibility = Visibility.none

class QuestPointsPerLevel(NamedRange):
    """
    The Number of quest points to increase the training range
    """
    display_name = "Quest Points per Training Level"
    default = 10
    range_start = 1
    range_end = 327
    special_range_names = {
        "disable" :327
    }

class LevelsPerQuestPoint(Range):
    """
    The number of levels to be expected to be over trained for each set of quest points
    """
    display_name = "Levels per Training Set"
    default = 1
    range_start = 0
    range_end = 10

class BaseTrainingLevels(NamedRange):
    """
    The Number of levels over a given training method you would be expected to train over by default
    """
    display_name = "Base Training Levels"
    default = 9
    range_start = 0
    range_end = 99
    special_range_names = {
        "disable":99
    }

class StartWithTutorialIsland(DefaultOnToggle):
    """
    Whether to keep or discard the starting inventory from tutorial island
    """
    display_name = "Start with Tutorial Island Items"

class PreCompletedTasks(LocationSet):
    """
    A list of location names that are completed before the game starts.
    Useful for cases where you need a quest to get to your starting area
    """
    display_name = "Pre-Completed Tasks"

class BannedChunks(OptionSet):
    """
    A list of chunks that won't be created as part of generation
    
    Uses internal names (e.g. "chunk_12338" not "South Draynor")
    But does count all sub-chunks (so you can just enter "chunk_8496" rather then "chunk_8496-1")
    """
    display_name = "Banned Chunks"


@dataclass
class OSRSMOptions(PerGameCommonOptions):
    starting_area: StartingArea
    goal_type: GoalType
    goal_location: GoalLocation
    bingo_size: BingoSize
    disable_chunk_culling: DisableChunkCulling
    disable_task_culling: DisableLocationCulling
    max_drop_rate: MaxDropRate
    full_drop_rate: FullMaxDropRate
    maximum_training_levels: MaxTrainingLevels
    starting_skill_levels: StartingLevels
    qp_per_level: QuestPointsPerLevel
    levels_per_qp: LevelsPerQuestPoint
    base_training_levels: BaseTrainingLevels
    tutorial_island_items: StartWithTutorialIsland
    pre_completed_tasks: PreCompletedTasks
    banned_chunks: BannedChunks
