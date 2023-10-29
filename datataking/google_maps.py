import googlemaps
from dotenv import load_dotenv
import requests
import os

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("maps_api_key"))


def get_place_id(search_term):
    try:
        place_result = gmaps.find_place(
            input=search_term,
            input_type="textquery",
            fields=["place_id"]
        )
        if place_result and place_result.get('candidates'):
            place_id = place_result['candidates'][0]['place_id']
            return place_id
        else:
            print(f"No place_id found for search term: {search_term}")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



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
    if not place_id:
        print("Invalid place_id")
        return None
    try:
        place_details = gmaps.place(
            place_id=place_id,
            fields=['photo']
        )
        if place_details and place_details.get('result', {}).get('photos'):
            photos = place_details['result']['photos']
            for index, photo in enumerate(photos):
                photo_reference = photo['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={os.getenv('maps_api_key')}"
                print(f"Photo {index + 1}: {photo_url}")
        else:
            print(f"No photos found for place_id: {place_id}")
    except Exception as e:
        print(f"An error occurred: {e}")


place_id = get_place_id('Ben Nevis, UK')
print(place_id)
print(get_photos(place_id))
