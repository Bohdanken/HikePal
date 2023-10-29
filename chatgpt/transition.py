from chatgpt.gpt_requests import ask_for_trails
from datataking.google_maps import get_place_id, get_photos, get_place_rating
from weather import weather

def extract_coordinates(trail_data):
    coordinates = []
    names=[]
    for name, tuples in trail_data.items():
        lat, lon = tuples["coordinates"].strip(' ()').split(',')
        coordinates.append((float(lat), float(lon)))
        names.append(name)
    return coordinates, names


def get_final_data(start_date,end_date, difficulty,city,radius):
    trail_data = ask_for_trails({"difficulty": difficulty, "city": city, "radius": radius})
    coordinates, names = extract_coordinates(trail_data)
    forecasts = []
    for i in range(len(coordinates)):
        coordinate = coordinates[i]
        forecasts.append(weather.forecast_between_dates_coordinates(
            longitude=coordinate[1],
            latitude=coordinate[0],
            start_date=start_date,
            end_date=end_date
        ))
        place_id = get_place_id(names[i])
        photos = get_photos(place_id)
        rating = get_place_rating(names[i])
        trail_data[names[i]]["weather"]=weather.good_weather(forecasts[-1])
        trail_data[names[i]]["photos"] = photos
        trail_data[names[i]]["rating"] = rating
        trail_data[names[i]]["coordinates"]= coordinate
    return trail_data

start_date = "2023-10-30"
end_date = "2023-11-01"
#print(get_final_data(start_date,end_date,"Moderate","Edinburgh",150))