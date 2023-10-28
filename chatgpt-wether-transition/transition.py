from chatgpt.gpt_requests import ask_for_trails
from weather import weather

def extract_coordinates(trail_data):
    coordinates = []
    for name, tubles in trail_data.items():
        # Split the coordinates into latitude and longitude components
        lat, lon = tubles["coordinates"].strip(' ()').split(',')
        coordinates.append((float(lat), float(lon)))

    return coordinates

start_date = "2023-11-01"
end_date = "2023-11-03"
trail_data = ask_for_trails({"city": "Sydney", "radius": 100})
coordinates = extract_coordinates(trail_data)
forecasts = []
estimate = []
for i in range(len(coordinates)):
    coordinate = coordinates[i]
    forecasts.append(weather.forecast_between_dates_coordinates(
        longitude=coordinate[1],
        latitude=coordinate[0],
        start_date=start_date,
        end_date=end_date
    ))
    estimate.append(weather.good_weather(forecasts[-1]))
print(forecasts)
print(estimate)