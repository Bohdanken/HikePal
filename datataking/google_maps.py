import googlemaps
from dotenv import load_dotenv
import requests
import os

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("maps_api_key"))


def get_place_id(search_term):
    try:
        autocomplete_result = gmaps.places_autocomplete(input_text=search_term)
        if autocomplete_result:
            refined_search_term = autocomplete_result[0]['description']
            place_result = gmaps.find_place(
                input=refined_search_term,
                input_type="textquery",
                fields=["place_id"]
            )
            if place_result and place_result.get('candidates'):
                place_id = place_result['candidates'][0]['place_id']
                return place_id
            else:
                print(f"No place_id found for refined search term: {refined_search_term}")
                return None
        else:
            print(f"No autocomplete suggestions found for search term: {search_term}")
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
    try:
        response = requests.get(endpoint_url, params=params)
        response.raise_for_status()  # Check for HTTP errors
        response_json = response.json()
    except requests.RequestException as e:  # Catch all requests exceptions
        print(f"Request error: {e}")
        return 0  # Return 0 on any request error
    if response_json.get('status') == 'OK' and response_json.get('results'):
        first_result = response_json['results'][0]
        return first_result.get('rating', 0)  # Return rating or 0 if rating is not present
    else:
        print(f"No rating found or API error for search term: {search_term}")
        return 0  # Return 0 if status is not 'OK' or results are empty


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
            result=[]
            for index, photo in enumerate(photos):
                photo_reference = photo['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={os.getenv('maps_api_key')}"
                result.append(f"{photo_url}")
            return result
        else:
            print(f"No photos found for place_id: {place_id}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_final_maps_result(location):
    place_id = get_place_id(location)
    photos=get_photos(place_id)
    rating=get_place_rating(location)
    print(photos)
    print(rating)

#get_final_maps_result("Campsie Glen")