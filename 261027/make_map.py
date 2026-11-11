import json

GEOJSON_PATH = "seoul_steps.geojson"
OUTPUT_PATH = "seoul_steps_map.html"

# file:// 에서 fetch 가 막히므로 데이터를 HTML 안에 직접 넣음
TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>서울 계단 (highway=steps)</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<style>html,body,#map{height:100%;margin:0}</style>
</head>
<body>
<div id="map"></div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const data = __DATA__;
const map = L.map("map").setView([37.5665, 126.978], 12);
// tile.openstreetmap.org 는 file:// (Referer 없음) 요청을 막아서 CARTO 타일 사용
L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png", {
  maxZoom: 19,
  subdomains: "abcd",
  attribution: "&copy; OpenStreetMap contributors &copy; CARTO"
}).addTo(map);
const layer = L.geoJSON(data, {
  style: { color: "#e63946", weight: 4 },
  onEachFeature: (f, l) => {
    const p = f.properties;
    const rows = Object.entries(p).map(([k, v]) => k + ": " + v).join("<br>");
    l.bindPopup(rows);
  }
}).addTo(map);
map.fitBounds(layer.getBounds());
</script>
</body>
</html>
"""


def main():
    with open(GEOJSON_PATH, encoding="utf-8") as f:
        data = f.read()
    html = TEMPLATE.replace("__DATA__", data)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"저장 -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
