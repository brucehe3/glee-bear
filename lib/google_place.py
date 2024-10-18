from google.maps import places_v1
from google.type import latlng_pb2
from google.maps.places_v1.types import SearchNearbyRequest
from .mock.data import shops


def combine_reviews(reviews):
    return ";".join([f"{review.text}" for review in reviews])


class GooglePlaceClient:
    def __init__(self, credentials):
        self.client = places_v1.PlacesClient(credentials=credentials)

    def get_photo(self, name, max_width_px=500, max_height_px=500):
        """get photo from google map photos"""

        request = places_v1.GetPhotoMediaRequest(name=name+"/media",
                                                 max_width_px=max_width_px,
                                                 max_height_px=max_height_px,
                                                 skip_http_redirect=True)

        response = self.client.get_photo_media(request=request)
        return response.photo_uri

    def sample_search_nearby(self, place_types, latitude, longitude, radius, mock=False):

        if mock:
            return shops
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
        response = self.client.search_nearby(request=request, metadata=metadata)

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
