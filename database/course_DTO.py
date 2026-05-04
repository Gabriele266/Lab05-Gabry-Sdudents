
from dataclasses import dataclass

@dataclass(frozen=True)
class CourseDTO:
    codins: str
    credits: int
    name: str
    pd: int

    def __hash__(self) -> int:
        return hash(self.codins)

    def __str__(self) -> str:
        return f"{self.name} ({self.codins})"