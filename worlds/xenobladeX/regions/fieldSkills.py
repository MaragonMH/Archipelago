from ..Regions import Requirement as Req, Rule 

def generate_field_skill_region(field_skill:str):
	return [ Rule("Menu"), *(Rule(f"{field_skill} {i}", {Req(f"FLDSK: {field_skill}", i)}) for i in range(1,5)) ]

mechanical_regions = generate_field_skill_region("Mechanical")
biological_regions = generate_field_skill_region("Biological")
archeological_regions = generate_field_skill_region("Archeological")