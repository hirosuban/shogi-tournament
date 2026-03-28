import json
from pathlib import Path


FRONTEND_DIR = Path("src/frontend")


def test_frontend_entry_files_exist() -> None:
    assert (FRONTEND_DIR / "index.html").exists()
    assert (FRONTEND_DIR / "style.css").exists()
    assert (FRONTEND_DIR / "app.js").exists()


def test_shutoken_geojson_contains_expected_prefectures() -> None:
    geojson_path = FRONTEND_DIR / "data" / "shutoken.geojson"
    payload = json.loads(geojson_path.read_text(encoding="utf-8"))

    assert payload["type"] == "FeatureCollection"
    names = {feature["properties"]["name"] for feature in payload["features"]}
    assert names == {"東京都", "神奈川県", "埼玉県", "千葉県"}
