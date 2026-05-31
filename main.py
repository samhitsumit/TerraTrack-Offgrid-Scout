import csv
import requests

# =========================
# CONFIG
# =========================
API_KEY = "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZ" \
"jYyNDgiLCJpZCI6IjFiZWQ2ODMwMzk0YTQ4ZjU4YjhhYmVk" \
"YWM2ZjBjMWE5IiwiaCI6Im11cm11cjY0In0="
CSV_FILE = "data.csv"
OUTPUT_KML = "output.kml"


# =========================
# READ CSV
# =========================
def read_csv(file_path):
    coords = []
    points_data = []

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                lat = float(row["lat"])
                lon = float(row["lon"])

                if lat == 0 or lon == 0:
                    continue

                coords.append([lon, lat])  # ORS expects [lon, lat]
                points_data.append(row)

            except Exception:
                continue

    return coords, points_data


# =========================
# ROUTE BETWEEN TWO POINTS (FIXED)
# =========================
def get_route(a, b):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "coordinates": [a, b],
        "radiuses": [2000, 2000]
    }

    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    if response.status_code != 200:
        print("Route error:", data)
        return []

    try:
        coords = data["features"][0]["geometry"]["coordinates"]
        return coords  # already [lon, lat]
    except Exception as e:
        print("Parse error:", e)
        return []


# =========================
# BUILD FULL ROUTE
# =========================
def build_full_route(coords):
    full_route = []

    for i in range(len(coords) - 1):
        start = coords[i]
        end = coords[i + 1]

        segment = get_route(start, end)

        if not segment:
            print(f"Skipping segment: {start} → {end}")
            continue

        if full_route:
            full_route.extend(segment[1:])  # avoid duplicates
        else:
            full_route.extend(segment)

    return full_route


# =========================
# CREATE KML
# =========================
def create_kml(points_data, route_coords, output_file):
    kml = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
'''

    # POINTS
    for p in points_data:
        kml += f"""
    <Placemark>
        <name>{p.get('date', '')} {p.get('time', '')}</name>
        <description>
            Temp: {p.get('temp', '')} C
            Humidity: {p.get('humidity', '')} %
        </description>
        <Point>
            <coordinates>{p['lon']},{p['lat']},0</coordinates>
        </Point>
    </Placemark>
"""

    # ROUTE LINE
    kml += """
    <Placemark>
        <name>Route</name>
        <Style>
            <LineStyle>
                <color>ff0000ff</color>
                <width>4</width>
            </LineStyle>
        </Style>
        <LineString>
            <tessellate>1</tessellate>
            <coordinates>
"""

    for lon, lat in route_coords:
        kml += f"{lon},{lat},0 "

    kml += """
            </coordinates>
        </LineString>
    </Placemark>
"""

    kml += """
</Document>
</kml>
"""

    with open(output_file, "w") as f:
        f.write(kml)


# =========================
# MAIN
# =========================
def main():
    coords, points_data = read_csv(CSV_FILE)

    print("Raw points:", len(coords))

    if len(coords) < 2:
        print("Not enough points")
        return

    # BUILD ROUTE (NO SNAPPING)
    route = build_full_route(coords)

    print("Route points:", len(route))

    if not route:
        print("No route generated")
        return

    create_kml(points_data, route, OUTPUT_KML)

    print("KML created:", OUTPUT_KML)


if __name__ == "__main__":
    main()