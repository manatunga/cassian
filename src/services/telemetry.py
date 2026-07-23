"""
High-level telemetry aggregation. Today: weather. Later: network, battery,
CPU, RAM, GPU, disk, temperature -- each living in its own services/ module
and rolled up here.
"""

from services import location, weather


def fetch_environment_reading(memory: dict):
    """
    Returns (reading, error_message). Exactly one of the two will be None.
    """
    lat, lon = location.get_coordinates(memory)
    reading, error = weather.fetch_current_conditions(lat, lon)
    return reading, error