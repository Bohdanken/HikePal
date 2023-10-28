import googlemaps
from dotenv import load_dotenv
import os

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv("AIzaSyDGyAoxcrGexAsnhwGGDVuWnUU2zunz2Lc"))
def get_place_data(hike_name):
    # Search for the place
    result = gmaps.places(query=hike_name)
    if result and result.get('results'):
        place = result['results'][0]
        place_id = place['place_id']
        # Get place details
        details = gmaps.place(place_id=place_id)
        # Extract rating and photos
        rating = details['result'].get('rating', None)
        photos = details['result'].get('photos', [])
        photo_urls = []
        for photo in photos:
            # Construct photo URL
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo['photo_reference']}&key=YOUR_API_KEY"
            photo_urls.append(photo_url)
        return rating, photo_urls


# List of hikes
hikes = ['Hike Name 1', 'Hike Name 2', ...]

# Get data for each hike
for hike in hikes:
    rating, photos = get_place_data(hike)
    print(f'Rating: {rating}, Photos: {photos}')