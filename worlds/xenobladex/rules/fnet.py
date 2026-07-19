import dataclasses
from typing import override
from BaseClasses import CollectionState
from rule_builder.rules import Has, Rule
from ..fnet.miranium import fnet_miranium_data
from ..fnet.credits import fnet_credits_data
from ..fnet.miranium import Mir
from ..fnet.credits import Crd


@dataclasses.dataclass()
class HasMiranium(Rule, game="Xenoblade X"):
    target: int

    @override
    def _instantiate(self, world) -> Rule.Resolved:
        # caching_enabled only needs to be passed in when your world inherits from CachedRuleBuilderWorld
        return self.Resolved(self.target, player=world.player,
                             caching_enabled=False)

    class Resolved(Rule.Resolved):
        target: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            st = state.count("DP: Storage Probe", self.player)
            dp = state.count("DP: Duplicator Probe", self.player)
            b1 = state.count("DP: Booster Probe G1", self.player)
            b2 = state.count("DP: Booster Probe G2", self.player)
            mech = state.count("FLDSK: Mechanical", self.player) + 1
            mir_state = Mir(st, dp, b1, b2, mech)
            miranium = 6  # fnet default
            for value, mirs in fnet_miranium_data.items():
                for mir in mirs:
                    possible = True
                    for it1, it2 in zip(dataclasses.astuple(mir), dataclasses.astuple(mir_state)):
                        possible = possible and it1 <= it2
                    if possible:
                        miranium = value
            return miranium >= self.target

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            # this function is only required if you have caching enabled
            return {
                "DP: Storage Probe": {id(self)},
                "DP: Duplicator Probe": {id(self)},
                "DP: Booster Probe G1": {id(self)},
                "DP: Booster Probe G2": {id(self)},
                "FLDSK: Mechanical": {id(self)},
            }


@dataclasses.dataclass()
class HasCredits(Rule, game="Xenoblade X"):
    target: int

    @override
    def _instantiate(self, world) -> Rule.Resolved:
        # caching_enabled only needs to be passed in when your world inherits from CachedRuleBuilderWorld
        return self.Resolved(self.target, player=world.player, caching_enabled=False)

    class Resolved(Rule.Resolved):
        target: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            r = [state.count(f"DP: Research Probe G{i}", self.player) for i in range(1, 7)]
            dp = state.count("DP: Duplicator Probe", self.player)
            b1 = state.count("DP: Booster Probe G1", self.player)
            b2 = state.count("DP: Booster Probe G2", self.player)
            mech = state.count("FLDSK: Mechanical", self.player) + 1
            crd_state = Crd(r[0], r[1], r[2], r[3], r[4], r[5], dp, b1, b2, mech)
            credits = 0
            for value, crds in fnet_credits_data.items():
                for crd in crds:
                    possible = True
                    for it1, it2 in zip(dataclasses.astuple(crd), dataclasses.astuple(crd_state)):
                        possible = possible and it1 <= it2
                    if possible:
                        credits = value
            return credits >= self.target

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            # this function is only required if you have caching enabled
            return {
                **{f"DP: Research Probe G{i}": {id(self)} for i in range(1, 7)},
                "DP: Duplicator Probe": {id(self)},
                "DP: Booster Probe G1": {id(self)},
                "DP: Booster Probe G2": {id(self)},
                "FLDSK: Mechanical": {id(self)},
            }


fnet_rules: dict[str, Rule] = {
    "FNet": Has("KEY: FNet"),
    "FNet Resource": Has("KEY: FNet"),
    # Boiled-Egg Ore, Ouroboros Crystal, Parhelion Platinum, Marine Rutile
    "FNet Resource 2": Has("KEY: FNet") & Has("FLDSK: Mechanical", 1),
    # Anything < 6k: 700, 750, 900, 1200, 1800, 2400, 2500, 3600, 4000, 4200, 5500, 5700
    "Miranium": Has("KEY: FNet"),
    "Miranium 7": Has("DP: Storage Probe"),
    "Miranium 10": HasMiranium(10),
    "Miranium 12": HasMiranium(12),
    "Miranium 15": HasMiranium(15),
    "Miranium 20": HasMiranium(20),
    "Miranium 30": HasMiranium(30),
    "Miranium 40": HasMiranium(40),
    "Miranium 50": HasMiranium(50),  # Ares 70
    "Miranium 100": HasMiranium(100),  # Ares 90
    # 3k just unlock all default mech 1 probes
    "Credits": Has("KEY: FNet"),
    "Credits 15": HasCredits(15),
    "Credits 70": HasCredits(70),
    "Credits 130": HasCredits(130),
}
