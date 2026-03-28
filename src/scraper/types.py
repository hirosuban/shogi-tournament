from dataclasses import dataclass
from datetime import date


@dataclass
class Tournament:
    date: date
    name: str
    venue: str
    prefecture: str
    categories: list[str]
    source_url: str
