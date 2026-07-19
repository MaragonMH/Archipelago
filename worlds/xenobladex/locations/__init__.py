from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Loc:
    name: str
    valid: bool = True
    rules: list[str] = field(default_factory=lambda: [])
    depends: list[str] = field(default_factory=lambda: [])
    type: Optional[int] = None
    id: Optional[int] = None
    prefix: Optional[str] = None
    required: bool = False

    def get_location(self):
        return f"{self.prefix}: {self.name}"

    def get_region(self):
        return "+".join(sorted(self.rules))
