from google.maps import places_v1
from google.type import latlng_pb2
from google.maps.places_v1.types import SearchNearbyRequest

from .mock.data import shops


def combine_reviews(reviews):
    return ";".join([f"{review.text}" for review in reviews])


def get_photo(name, max_width_px=500, max_height_px=500):
    """get photo from google map photos"""
    client = places_v1.PlacesClient()
    request = places_v1.GetPhotoMediaRequest(name=name+"/media",
                                             max_width_px=max_width_px,
                                             max_height_px=max_height_px,
                                             skip_http_redirect=True)

    response = client.get_photo_media(request=request)
    return response.photo_uri


def sample_search_nearby(place_types, latitude, longitude, radius, mock=False):

    if mock:
        return shops

    # Create a client
    client = places_v1.PlacesClient()
    center_point = latlng_pb2.LatLng(latitude=latitude, longitude=longitude)

    # Initialize request argument(s)
    location_restriction = SearchNearbyRequest.LocationRestriction()
    location_restriction.circle.radius = radius
    location_restriction.circle.center = center_point

    request = SearchNearbyRequest(
        location_restriction=location_restriction,
        included_types=[item.strip() for item in place_types.split(",")]
    )
    # 设置 metadata 传递 FieldMask
    metadata = [("x-goog-fieldmask", "places.id,places.displayName,places.photos,places.formattedAddress,"
                                     "places.location.latitude,places.location.longitude,"
                                     "places.rating,places.googleMapsUri,"
                                     "places.reviews.text,places.reviews.rating")]

    # Make the request
    response = client.search_nearby(request=request, metadata=metadata)

    # Handle the response
    result = []
    for index, place in enumerate(response.places):
        result.append({
            'index': index+1,
            'name': place.display_name,
            'photos': place.photos,
            'latitude': place.location.latitude,
            'longitude': place.location.longitude,
            'address': place.formatted_address,
            'rating': place.rating,
            'google_map_uri': place.google_maps_uri,
            'reviews': combine_reviews(place.reviews),
        })

    return result


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('../.env')
    # print(sample_search_nearby("chinese_restaurant, indonesian_restaurant", 1.3920613, 103.913496, 5000, mock=False))
    print(get_photo("places/ChIJK8rh97sV2jERksUCQ2Ugtcc/photos/AdCG2DOXYQWp7THCk_t1bInHKIwtjWROfSD5KnRbit8yy9aBIX4u7krDJ7w0bJW-lhq5RWPoqAjPwm75eaVpRmTcF8dz8qlLJfrVtD7JSkkRhco658-2X8YbYjULL1imXTJ9VVE_um9gOlkq3s8mS5d2aq-H2-DIdZWilK-E/media"))