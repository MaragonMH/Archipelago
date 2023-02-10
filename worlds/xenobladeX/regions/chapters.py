from ..dataType import Requirement as Req, Rule 

chapter_regions = [
Rule("Menu"),
Rule("Chapter 1"),
Rule("Chapter 2"),
Rule("Chapter 3"),
Rule("Chapter 4"),
Rule("Chapter 5", [Req("Mining Probe G1", 3), Req("Research Probe G1"), Req("FNet")]),
Rule("Chapter 6"),
Rule("Chapter 7"),
Rule("Chapter 8"),
Rule("Chapter 9", [Req("Lao Heart")]),
Rule("Chapter 10"),
Rule("Chapter 11"),
Rule("Chapter 12", [Req("Gwin Heart")]),
Rule("Epilogue", [Req("Skell License"), Req("Flight Module")]),
]