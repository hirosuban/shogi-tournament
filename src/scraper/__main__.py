"""Entry point for the scraper.

Usage:
    uv run python -m src.scraper
"""

import logging
import sys

from .config import CONFIG
from .service import run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)


def main() -> None:
    try:
        run_pipeline(CONFIG)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()
