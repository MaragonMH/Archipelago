from typing import List
from ..Regions import Requirement as Req, Rule


def generate_field_skill_region(field_skill: str) -> List[Rule]:
    return [Rule("Menu"), *(Rule(f"{field_skill} {i}", {Req(f"FLDSK: {field_skill}", i - 1)}) for i in range(1, 6))]


mechanical_regions: List[Rule] = generate_field_skill_region("Mechanical")
biological_regions: List[Rule] = generate_field_skill_region("Biological")
archeological_regions: List[Rule] = generate_field_skill_region("Archeological")

fnet_precious_ressources_regions: List[Rule] = [
    Rule("Menu"),
    # all others
    Rule("FNet Resource"),
    # Boiled-Egg Ore, Ouroboros Crystal, Parhelion Platinum, Marine Rutile
    Rule("FNet Resource 2", {Req("FLDSK: Mechanical", 1)})
]
