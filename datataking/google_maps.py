import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("maps_api_key"))
def get_place_data(hike_name):
    result = gmaps.places(query=hike_name)
    if result and result.get('results'):
        place = result['results'][0]
        place_id = place['place_id']
        details = gmaps.place(place_id=place_id)
        rating = details['result'].get('rating', None)
        photos = details['result'].get('photos', [])
        photo_urls = []
        for photo in photos:
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key={os.getenv('maps_api_key')}"
            photo_urls.append(photo_url)
        return rating, photo_urls



hikes = ['West Highland Way']
for hike in hikes:
    rating, photos = get_place_data(hike)
    print(f'Rating: {rating}, Photos: {photos}')