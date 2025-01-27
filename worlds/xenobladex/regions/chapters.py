from typing import List
from ..Regions import Requirement as Req, Rule

# flake8: noqa
chapter_regions: List[Rule] = [
Rule("Menu"),
Rule("Chapter 1"),
Rule("Chapter 2"),
Rule("Chapter 3"),
Rule("Chapter 4", {Req("KEY: Blade License"), Req("DP: Mining Probe G1", 3), Req("DP: Research Probe G1"), Req("KEY: FNet")}),
Rule("Chapter 5"),
Rule("Chapter 6"),
Rule("Chapter 7"),
Rule("Chapter 8", {Req("FRD: Lao")}),
Rule("Chapter 9"),
Rule("Chapter 10"),
Rule("Chapter 11", {Req("FRD: Gwin")}),
Rule("Chapter 12", {Req("KEY: Skell License"), Req("KEY: Flight Module")}),
]
