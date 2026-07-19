import dataclasses
from typing import cast, override
from rule_builder.field_resolvers import FieldResolver
from rule_builder.rules import Has, Rule
from worlds.AutoWorld import World
from ..Options import XenobladeXOptions


# Convert the logic level into the required logic count
def get_logic_level_count(logic_level: int, step_size: int):
    return int(min(logic_level, 50) / step_size) + int(min(logic_level - 50, 0) / (step_size + 5))


@dataclasses.dataclass(frozen=True)
class LogicLevelResolver(FieldResolver, game="Xenoblade X"):
    logic_level: int

    @override
    def resolve(self, world: "World") -> int:
        step_size = cast(XenobladeXOptions, world.options).logic_level_steps.value
        count = get_logic_level_count(self.logic_level, step_size)
        return count

    @override
    def __str__(self) -> str:
        return f"(Lvl {self.logic_level})"


level_rules: dict[str, Rule] = {
    "Lvl 1": Has("KEY: Level", count=LogicLevelResolver(1)),
    "Lvl 2": Has("KEY: Level", count=LogicLevelResolver(2)),
    "Lvl 3": Has("KEY: Level", count=LogicLevelResolver(3)),
    "Lvl 4": Has("KEY: Level", count=LogicLevelResolver(4)),
    "Lvl 5": Has("KEY: Level", count=LogicLevelResolver(5)),
    "Lvl 6": Has("KEY: Level", count=LogicLevelResolver(6)),
    "Lvl 7": Has("KEY: Level", count=LogicLevelResolver(7)),
    "Lvl 8": Has("KEY: Level", count=LogicLevelResolver(8)),
    "Lvl 9": Has("KEY: Level", count=LogicLevelResolver(9)),
    "Lvl 10": Has("KEY: Level", count=LogicLevelResolver(10)),
    "Lvl 11": Has("KEY: Level", count=LogicLevelResolver(11)),
    "Lvl 12": Has("KEY: Level", count=LogicLevelResolver(12)),
    "Lvl 13": Has("KEY: Level", count=LogicLevelResolver(13)),
    "Lvl 14": Has("KEY: Level", count=LogicLevelResolver(14)),
    "Lvl 15": Has("KEY: Level", count=LogicLevelResolver(15)),
    "Lvl 16": Has("KEY: Level", count=LogicLevelResolver(16)),
    "Lvl 17": Has("KEY: Level", count=LogicLevelResolver(17)),
    "Lvl 18": Has("KEY: Level", count=LogicLevelResolver(18)),
    "Lvl 19": Has("KEY: Level", count=LogicLevelResolver(19)),
    "Lvl 20": Has("KEY: Level", count=LogicLevelResolver(20)),
    "Lvl 21": Has("KEY: Level", count=LogicLevelResolver(21)),
    "Lvl 22": Has("KEY: Level", count=LogicLevelResolver(22)),
    "Lvl 23": Has("KEY: Level", count=LogicLevelResolver(23)),
    "Lvl 24": Has("KEY: Level", count=LogicLevelResolver(24)),
    "Lvl 25": Has("KEY: Level", count=LogicLevelResolver(25)),
    "Lvl 26": Has("KEY: Level", count=LogicLevelResolver(26)),
    "Lvl 27": Has("KEY: Level", count=LogicLevelResolver(27)),
    "Lvl 28": Has("KEY: Level", count=LogicLevelResolver(28)),
    "Lvl 29": Has("KEY: Level", count=LogicLevelResolver(29)),
    "Lvl 30": Has("KEY: Level", count=LogicLevelResolver(30)),
    "Lvl 31": Has("KEY: Level", count=LogicLevelResolver(31)),
    "Lvl 32": Has("KEY: Level", count=LogicLevelResolver(32)),
    "Lvl 33": Has("KEY: Level", count=LogicLevelResolver(33)),
    "Lvl 34": Has("KEY: Level", count=LogicLevelResolver(34)),
    "Lvl 35": Has("KEY: Level", count=LogicLevelResolver(35)),
    "Lvl 36": Has("KEY: Level", count=LogicLevelResolver(36)),
    "Lvl 37": Has("KEY: Level", count=LogicLevelResolver(37)),
    "Lvl 38": Has("KEY: Level", count=LogicLevelResolver(38)),
    "Lvl 39": Has("KEY: Level", count=LogicLevelResolver(39)),
    "Lvl 40": Has("KEY: Level", count=LogicLevelResolver(40)),
    "Lvl 41": Has("KEY: Level", count=LogicLevelResolver(41)),
    "Lvl 42": Has("KEY: Level", count=LogicLevelResolver(42)),
    "Lvl 43": Has("KEY: Level", count=LogicLevelResolver(43)),
    "Lvl 44": Has("KEY: Level", count=LogicLevelResolver(44)),
    "Lvl 45": Has("KEY: Level", count=LogicLevelResolver(45)),
    "Lvl 46": Has("KEY: Level", count=LogicLevelResolver(46)),
    "Lvl 47": Has("KEY: Level", count=LogicLevelResolver(47)),
    "Lvl 48": Has("KEY: Level", count=LogicLevelResolver(48)),
    "Lvl 49": Has("KEY: Level", count=LogicLevelResolver(49)),
    "Lvl 50": Has("KEY: Level", count=LogicLevelResolver(50)),
    "Lvl 51": Has("KEY: Level", count=LogicLevelResolver(51)),
    "Lvl 52": Has("KEY: Level", count=LogicLevelResolver(52)),
    "Lvl 53": Has("KEY: Level", count=LogicLevelResolver(53)),
    "Lvl 54": Has("KEY: Level", count=LogicLevelResolver(54)),
    "Lvl 55": Has("KEY: Level", count=LogicLevelResolver(55)),
    "Lvl 56": Has("KEY: Level", count=LogicLevelResolver(56)),
    "Lvl 57": Has("KEY: Level", count=LogicLevelResolver(57)),
    "Lvl 58": Has("KEY: Level", count=LogicLevelResolver(58)),
    "Lvl 59": Has("KEY: Level", count=LogicLevelResolver(59)),
    "Lvl 60": Has("KEY: Level", count=LogicLevelResolver(60)),
    "Lvl 61": Has("KEY: Level", count=LogicLevelResolver(61)),
    "Lvl 62": Has("KEY: Level", count=LogicLevelResolver(62)),
    "Lvl 63": Has("KEY: Level", count=LogicLevelResolver(63)),
    "Lvl 64": Has("KEY: Level", count=LogicLevelResolver(64)),
    "Lvl 65": Has("KEY: Level", count=LogicLevelResolver(65)),
    "Lvl 66": Has("KEY: Level", count=LogicLevelResolver(66)),
    "Lvl 67": Has("KEY: Level", count=LogicLevelResolver(67)),
    "Lvl 68": Has("KEY: Level", count=LogicLevelResolver(68)),
    "Lvl 69": Has("KEY: Level", count=LogicLevelResolver(69)),
    "Lvl 70": Has("KEY: Level", count=LogicLevelResolver(70)),
    "Lvl 71": Has("KEY: Level", count=LogicLevelResolver(71)),
    "Lvl 72": Has("KEY: Level", count=LogicLevelResolver(72)),
    "Lvl 73": Has("KEY: Level", count=LogicLevelResolver(73)),
    "Lvl 74": Has("KEY: Level", count=LogicLevelResolver(74)),
    "Lvl 75": Has("KEY: Level", count=LogicLevelResolver(75)),
    "Lvl 76": Has("KEY: Level", count=LogicLevelResolver(76)),
    "Lvl 77": Has("KEY: Level", count=LogicLevelResolver(77)),
    "Lvl 78": Has("KEY: Level", count=LogicLevelResolver(78)),
    "Lvl 79": Has("KEY: Level", count=LogicLevelResolver(79)),
    "Lvl 80": Has("KEY: Level", count=LogicLevelResolver(80)),
    "Lvl 81": Has("KEY: Level", count=LogicLevelResolver(81)),
    "Lvl 82": Has("KEY: Level", count=LogicLevelResolver(82)),
    "Lvl 83": Has("KEY: Level", count=LogicLevelResolver(83)),
    "Lvl 84": Has("KEY: Level", count=LogicLevelResolver(84)),
    "Lvl 85": Has("KEY: Level", count=LogicLevelResolver(85)),
    "Lvl 86": Has("KEY: Level", count=LogicLevelResolver(86)),
    "Lvl 87": Has("KEY: Level", count=LogicLevelResolver(87)),
    "Lvl 88": Has("KEY: Level", count=LogicLevelResolver(88)),
    "Lvl 89": Has("KEY: Level", count=LogicLevelResolver(89)),
    "Lvl 90": Has("KEY: Level", count=LogicLevelResolver(90)),
    "Lvl 91": Has("KEY: Level", count=LogicLevelResolver(91)),
    "Lvl 92": Has("KEY: Level", count=LogicLevelResolver(92)),
    "Lvl 93": Has("KEY: Level", count=LogicLevelResolver(93)),
    "Lvl 94": Has("KEY: Level", count=LogicLevelResolver(94)),
    "Lvl 95": Has("KEY: Level", count=LogicLevelResolver(95)),
    "Lvl 96": Has("KEY: Level", count=LogicLevelResolver(96)),
    "Lvl 97": Has("KEY: Level", count=LogicLevelResolver(97)),
    "Lvl 98": Has("KEY: Level", count=LogicLevelResolver(98)),
    "Lvl 99": Has("KEY: Level", count=LogicLevelResolver(99)),
}
