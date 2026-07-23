"""
Stores meta data about the user: name, location, preferences 
(eventually voice profile, timezone, units, language).
Also contains the shape of the brand-new memory file that initiates during Cassian's first time booting.
"""

import hashlib
from core.constants import DEFAULT_CREATOR, DEFAULT_LOCATION, COMMAND_INDEX

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def verify_password(memory: dict, input_password: str) -> bool:
    stored_hash = memory.get('auth', {}).get('password_hash')
    if not stored_hash:
        return False
    return hash_password(input_password) == stored_hash


def create_memory(
        version: str, 
        user: str = DEFAULT_CREATOR,
        city: str = 'Unknown', 
        location: dict = DEFAULT_LOCATION,
        password: str = ''
) -> dict:
    return {
        'system_name': 'Cassian',
        'version': version,
        'user': user,
        'boot_count': 1,
        'location': {
            'city': city,
            'lat': location.get('lat', DEFAULT_LOCATION['lat']),
            'lon': location.get('lon', DEFAULT_LOCATION['lon'])
        },
        'auth': {
            'password_hash': hash_password(password) if password else None
        },
        'notes': [],
        'commands': COMMAND_INDEX,
        'task_queue': [] 
    }

def update_user_name(memory: dict, new_name: str) -> None:
    memory['user'] = new_name

def update_user_city(memory: dict, new_city: str, lat: float, lon: float) -> None:
    if 'location' not in memory:
        memory['location'] = []
    memory['location']['city'] = new_city
    memory['location']['lat'] = lat
    memory['location']['lon'] = lon