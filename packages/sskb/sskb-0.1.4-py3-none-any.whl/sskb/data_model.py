from typing import Self, Any
from dataclasses import dataclass, field
from saf import Sentence


@dataclass
class Entity:
    surface: str
    kbid: str
    metadata: dict[str, Any] = field(default_factory=dict)
    synonyms: list[Self] = field(default_factory=list)
    hypernyms: list[Self] = field(default_factory=list)


class Statement(Sentence):
    def __init__(self, surface: str):
        super().__init__()
        self.surface: str = surface
        self.premises: list[Self] = list()
        self.entities: list[Entity] = list()


