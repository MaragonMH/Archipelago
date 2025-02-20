from typing import List
from ..Regions import Requirement as Req, Rule

# flake8: noqa
chapter_regions: List[Rule] = [
Rule("Menu"),
Rule("Chapter 1"),
Rule("Chapter 2"),
Rule("Chapter 3"),
Rule("Chapter 4", {Req("KEY: Blade License"), Req("DP: Mining Probe G1", 3), Req("DP: Research Probe G1"), Req("KEY: FNet"), Req("PRIM", 14)}),
Rule("Chapter 5"),
Rule("Chapter 6", {Req("NOCT", 16)}),
Rule("Chapter 7", {Req("OBLI", 24)}),
Rule("Chapter 8", {Req("FRD: Lao"), Req("MIRA", 70)}),
Rule("Chapter 9"),
Rule("Chapter 10", {Req("SYLV", 14)}),
Rule("Chapter 11", {Req("FRD: Gwin"), Req("CAUL", 8)}),
Rule("Chapter 12", {Req("KEY: Skell License"), Req("SKF"), Req("KEY: Flight Module")}),
]
