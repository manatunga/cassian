"""
Responsible for converting a location (user's city of residence) into coordinates Cassian can use,
and for reading the coordinates currently stored in memory.

Currently this is just a lookup with sane fallbacks. Eventually: reverse
geocoding, timezone resolution, country detection (likely via a real geocoding
library such as geopy, per requirements.txt).
"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from ui import terminal
from core.constants import DEFAULT_LOCATION

def get_coordinates(memory: dict):
    location = memory.get('location', {})
    lat = location.get('lat', DEFAULT_LOCATION['lat'])
    lon = location.get('lon', DEFAULT_LOCATION['lon'])
    return float(lat), float(lon)

def city_to_coordinates(city_name: str):
    """
    Placeholder for future geocoding (e.g. via geopy). 
    Returns a (lat, lon) tuple if found, or None if the lookup fails.
    """

    if not city_name or not city_name.strip():
        return None

    geolocator = Nominatim(user_agent='CassianAssistant')

    try:
        location = geolocator.geocode(city_name.strip(), timeout=5)
        if location:
            return float(location.latitude), float(location.longitude)
    except (GeocoderTimedOut, GeocoderServiceError) as error:
        terminal.print_error(f"Uh oh. Geocoding service error for '{city_name}': {error}")
    except Exception as error:
        terminal.print_error(f"Uh oh. Unexpected error during geocoding for '{city_name}': {error}")
        
    return None