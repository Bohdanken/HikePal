from chatgpt.gpt_requests import ask_for_trails


def extract_coordinates(trail_data):
    coordinates = []

    for name, coords in trail_data.items():
        # Split the coordinates into latitude and longitude components
        lat, lon = coords.strip(' ()').split(',')
        coordinates.append((float(lat), float(lon)))

    return coordinates


trail_data = ask_for_trails({"city": "Sydney", "radius": 100})
coordinates = extract_coordinates(trail_data)

print(coordinates)
