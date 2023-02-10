from typing import NamedTuple


class Data(NamedTuple):
	name: str
	valid: bool = True
	count: int = 1

class Requirement(NamedTuple):
	name: str
	count: int = 1

class Rule(NamedTuple):
    region: str
    requirements: list[Requirement] = []