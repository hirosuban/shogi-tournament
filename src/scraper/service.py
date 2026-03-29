import json
import logging

from .config import Config
from .parser import filter_kanto, scrape

logger = logging.getLogger(__name__)


def run_pipeline(config: Config) -> None:
    """Full pipeline: scrape → filter → write JSON."""
    try:
        all_tournaments = scrape(config)
    except ValueError as exc:
        logger.error("Scraping failed (structure change detected): %s", exc)
        raise
    except Exception as exc:
        logger.error("Scraping failed (network/parse error): %s", exc)
        raise

    kanto = filter_kanto(all_tournaments, config)
    if not kanto:
        logger.warning("No Kanto tournaments found — possible data issue")

    kanto.sort(key=lambda t: t.date)

    records = [
        {
            "date": t.date.isoformat(),
            "name": t.name,
            "venue": t.venue,
            "prefecture": t.prefecture,
            "category": ",".join(t.categories),
            "source_url": t.source_url,
        }
        for t in kanto
    ]

    config.output_path.parent.mkdir(parents=True, exist_ok=True)
    config.output_path.write_text(
        json.dumps(records, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    logger.info(
        "Pipeline complete: %d records written to %s",
        len(records),
        config.output_path,
    )
