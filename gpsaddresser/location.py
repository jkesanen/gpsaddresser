from dataclasses import dataclass

from geopy import distance
from geopy.geocoders import Nominatim

@dataclass
class Location:
    """A Class for storing a location point."""
    latitude: float
    longitude: float
    altitude: int = 0
    address: str = ''

    def get_coordinates(self) -> (float, float):
        """Returns latitude and longitude as a tuple."""
        return self.latitude, self.longitude


def location_distance_kilometers(a: Location, b: Location) -> float:
    """Calculates the distance between two points.

    Returns:
        A number of kilometers between two point.
    """
    return distance.distance(a.get_coordinates(), b.get_coordinates())


def location_distance_meters(a: Location, b: Location) -> float:
    """Calculates the distance between two points.

    Returns:
        A number of meters between two points.
    """
    return location_distance_kilometers(a, b).m


def location_distance_miles(a: Location, b: Location) -> float:
    """Calculates the distance between two points.

    Returns:
        A number of miles between two points.
    """
    return location_distance_kilometers(a, b).mi


def address_to_location(address: str) -> Location:
    """Queries location coordinates for a given street address.

    Returns:
        A number of miles between two points.
    """
    geolocator = Nominatim(user_agent="FIT-sorter")
    response = geolocator.geocode(address)

    if response:
        return Location(response.latitude, response.longitude)

    return None
