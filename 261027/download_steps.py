import json

import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OUTPUT_PATH = "seoul_steps.geojson"

QUERY = """
[out:json][timeout:120];
area["name:ko"="서울특별시"]["admin_level"="4"]->.a;
way["highway"="steps"](area.a);
out geom tags;
"""


def fetch_ways():
    # Overpass 는 기본 python-requests User-Agent 를 406 으로 거절함
    headers = {"User-Agent": "seoul-steps-downloader/0.1"}
    res = requests.post(OVERPASS_URL, data={"data": QUERY}, headers=headers, timeout=180)
    res.raise_for_status()
    return res.json()["elements"]


def to_feature(way):
    coords = [[p["lon"], p["lat"]] for p in way["geometry"]]
    return {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": coords},
        "properties": {"id": way["id"], **way.get("tags", {})},
    }


def main():
    ways = fetch_ways()
    fc = {"type": "FeatureCollection", "features": [to_feature(w) for w in ways]}
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(fc, f, ensure_ascii=False)
    print(f"{len(fc['features'])}개 저장 -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
