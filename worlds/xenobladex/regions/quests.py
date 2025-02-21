from ..Regions import Requirement as Req, Rule

# flake8: noqa
# Probe-fessional
quest_probe_fessional_regions: list[Rule] = [
Rule("Menu"),
Rule("Quest Probe-fessional", {Req("DP: Mining Probe G1", 3), Req("DP: Research Probe G1"), Req("KEY: FNet")}),
]

# The Skell License
quest_skell_license_regions: list[Rule] = [
Rule("Menu"),
Rule("Quest Skell License", {Req("WPN: Trial Knife"), Req("WPN: Trial Assault Rifle"), Req("WPN: Trial Sword")}),
]

quest_regions: list[Rule] = [
    *quest_probe_fessional_regions,
    *quest_skell_license_regions,
]
