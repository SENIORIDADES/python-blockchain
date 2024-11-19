from geopy.geocoders import Nominatim
from .jsonService import JsonService
import random
import math

class LocationService():

  @staticmethod
  def _get_location_name(latitude: float, longitude: float):
    geolocation = Nominatim(user_agent="geoapi")
    location = geolocation.reverse((latitude, longitude),
                                   language='en', exactly_one=True)
    if location:
      address = location.raw.get('address', {})
      ocean = address.get('sea', None)
      return ocean
    return None