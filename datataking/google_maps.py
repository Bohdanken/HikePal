import googlemaps
from dotenv import load_dotenv
import requests
import os

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("maps_api_key"))


def get_place_id(search_term):
    endpoint_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': search_term,
        'key': os.getenv("maps_api_key")
    }
    response = requests.get(endpoint_url, params=params)
    response_json = response.json()
    place_id = response_json['results'][0]['place_id']
    return place_id


def get_place_rating(search_term):
    endpoint_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'query': search_term,
        'key': os.getenv("maps_api_key")
    }
    response = requests.get(endpoint_url, params=params)
    response_json = response.json()
    return response_json['results'][0]['rating']


def get_photos(place_id):
    endpoint_url = f"https://maps.googleapis.com/maps/api/place/details/json"
    API_KEY=os.getenv("maps_api_key")
    params = {
        'placeid': place_id,
        'key': API_KEY,
        'fields': 'photo'
    }
    response = requests.get(endpoint_url, params=params)
    response_json = response.json()
    photos = response_json['result']['photos']
    for index, photo in enumerate(photos):
        photo_reference = photo['photo_reference']
        photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={API_KEY}"
        print(f"Photo {index + 1}: {photo_url}")


# Replace 'Eiffel Tower' with the name of the place you are interested in
place_id = get_place_id('Conic Hill, UK')
print(place_id)
print(get_photos(place_id))
