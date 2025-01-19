from ..Regions import Requirement as Req, Rule 

chapter_regions = [
Rule("Menu"),
Rule("Chapter 1"),
Rule("Chapter 2"),
Rule("Chapter 3"),
Rule("Chapter 4"),
Rule("Chapter 5", {Req("DP: Mining Probe G1", 3), Req("DP: Research Probe G1"), Req("KEY: FNet")}),
Rule("Chapter 6"),
Rule("Chapter 7"),
Rule("Chapter 8"),
Rule("Chapter 9", {Req("FRD: Lao")}),
Rule("Chapter 10"),
Rule("Chapter 11"),
Rule("Chapter 12", {Req("FRD: Gwin")}),
Rule("Epilogue", {Req("KEY: Skell License"), Req("KEY: Flight Module")}),
]