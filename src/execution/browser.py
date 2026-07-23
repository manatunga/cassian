"""
Only responsible for opening a browser: google.com, a search results page, or
a direct URL. Nothing else lives here.

Tries to open specifically in Chrome (matching Cassian's original behaviour)
by locating it per-OS; if Chrome can't be found, falls back gracefully to
whatever the system's default browser is, via Python's built-in `webbrowser`
module -- so Cassian never simply fails to open a link just because Chrome
isn't installed at the expected location.
"""

import shutil
import urllib.parse
import webbrowser
from pathlib import Path

from utils import platform_utils

# Known install locations / executable names per OS, checked in order.
_CHROME_CANDIDATES = {
    "windows": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ],
    "mac": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ],
    "linux": [
        "google-chrome",
        "google-chrome-stable",
        "chromium-browser",
        "chromium",
    ],
}


def find_chrome_path():
    """
    Returns a usable Chrome path/command for this OS, or None if Chrome
    couldn't be located anywhere Cassian knows to look.
    """
    system = platform_utils.get_os()
    for candidate in _CHROME_CANDIDATES.get(system, []):
        if Path(candidate).exists() or shutil.which(candidate):
            return candidate
    return None


def _open(url: str):
    chrome_path = find_chrome_path()
    if chrome_path:
        try:
            # webbrowser's generic-browser template: %s is replaced with the URL.
            controller = webbrowser.get(f'"{chrome_path}" %s')
            controller.open(url)
            return
        except webbrowser.Error:
            pass  # fall through to the system default browser below

    webbrowser.open(url)


def open_google():
    _open('https://google.com')


def open_url(url: str):
    _open(url)


def open_target_url(target: str) -> bool:
    if not target:
        return False

    url = target
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url

    open_url(url)
    return True


def search_google(query: str):
    encoded_query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={encoded_query}"
    _open(search_url)


def try_handle(action: str) -> bool:
    """
    Returns True if `action` was a browser-related target (chrome/google, or
    a bare http(s) URL) and was launched, False otherwise.
    """
    if 'chrome' in action or 'google chrome' in action or 'google' in action:
        open_google()
        return True
    if action.startswith('http://') or action.startswith('https://'):
        open_url(action)
        return True
    return False
