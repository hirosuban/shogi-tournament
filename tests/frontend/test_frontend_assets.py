import json
from pathlib import Path


FRONTEND_DIR = Path("src/frontend")


def test_frontend_entry_files_exist() -> None:
    assert (FRONTEND_DIR / "index.html").exists()
    assert (FRONTEND_DIR / "style.css").exists()
    assert (FRONTEND_DIR / "app.js").exists()


def test_frontend_loads_local_json() -> None:
    app_js = (FRONTEND_DIR / "app.js").read_text(encoding="utf-8")

    assert "http://localhost:8000" not in app_js
    assert "tournaments.json" in app_js


def test_tournaments_json_exists_and_valid() -> None:
    json_path = FRONTEND_DIR / "data" / "tournaments.json"
    payload = json.loads(json_path.read_text(encoding="utf-8"))

    assert isinstance(payload, list)
    assert len(payload) > 0
    first = payload[0]
    assert "date" in first
    assert "name" in first
    assert "venue" in first
    assert "prefecture" in first
    assert "category" in first
    assert "source_url" in first


def test_shutoken_geojson_contains_expected_prefectures() -> None:
    geojson_path = FRONTEND_DIR / "data" / "shutoken.geojson"
    payload = json.loads(geojson_path.read_text(encoding="utf-8"))

    assert payload["type"] == "FeatureCollection"
    names = {feature["properties"]["name"] for feature in payload["features"]}
    assert names == {"東京都", "神奈川県", "埼玉県", "千葉県"}
