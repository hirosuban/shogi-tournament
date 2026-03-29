from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Config:
    source_url: str = "https://sho-shogi.blogspot.com/p/blog-page_20.html?m=1"
    output_path: Path = field(
        default_factory=lambda: Path("src/frontend/data/tournaments.json")
    )
    kanto_prefectures: frozenset[str] = field(
        default_factory=lambda: frozenset(["東京都", "神奈川県", "埼玉県", "千葉県"])
    )


CONFIG = Config()
