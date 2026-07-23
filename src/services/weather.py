"""
Fetches raw weather forecast data from Open-Meteo API based on user's location:
temperature (eventually humidity, wind, etc. once Cassian needs them).
"""

import json
import urllib.request
from urllib.error import HTTPError, URLError

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

def fetch_current_conditions(lat: float, lon: float):
    # Returns the parsed JSON response, or None if request failed (along with error)

    url = f"{OPEN_METEO_URL}?latitude={lat}&longitude={lon}&current=temperature_2m"

    try:
        request = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windoes NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode('utf-8')
            return json.loads(raw), None
    except HTTPError as error:
        return None, f"Server responded with HTTP status code {error.code}"
    except URLError as err:
        return None, f"Failed to reach server. Reason: {err.reason}"