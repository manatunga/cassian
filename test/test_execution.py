"""
Tests for execution/dispatcher.py, execution/applications.py and
execution/browser.py: run app, open URL, dispatcher routing, and
cross-platform behaviour.
"""

from unittest.mock import patch

from execution import applications, browser, system_open
from execution.dispatcher import execute_action
from utils import platform_utils


def test_dispatcher_routes_known_app_to_applications(monkeypatch):
    monkeypatch.setattr(applications, "launch_application", lambda action: True)
    assert execute_action("notepad") is True


def test_dispatcher_routes_url_to_browser(monkeypatch):
    monkeypatch.setattr(applications, "launch_application", lambda action: False)
    with patch("execution.browser.open_url") as mock_open:
        result = execute_action("https://example.com")
        assert result is True
        mock_open.assert_called_once()


def test_dispatcher_returns_false_for_unrecognized_action(monkeypatch):
    monkeypatch.setattr(applications, "launch_application", lambda action: False)
    monkeypatch.setattr(browser, "try_handle", lambda action: False)
    assert execute_action("some nonsense action") is False


def test_platform_utils_reports_a_known_os():
    assert platform_utils.get_os() in ("windows", "mac", "linux")


def test_system_open_uses_xdg_open_on_linux(monkeypatch):
    monkeypatch.setattr(platform_utils, "get_os", lambda: "linux")
    with patch("subprocess.Popen") as mock_popen:
        result = system_open.open_with_os_default("spotify://")
        assert result is True
        mock_popen.assert_called_once_with(["xdg-open", "spotify://"])


def test_system_open_uses_open_on_mac(monkeypatch):
    monkeypatch.setattr(platform_utils, "get_os", lambda: "mac")
    with patch("subprocess.Popen") as mock_popen:
        result = system_open.open_with_os_default("spotify://")
        assert result is True
        mock_popen.assert_called_once_with(["open", "spotify://"])


def test_system_open_uses_start_on_windows(monkeypatch):
    monkeypatch.setattr(platform_utils, "get_os", lambda: "windows")
    with patch("subprocess.Popen") as mock_popen:
        result = system_open.open_with_os_default("spotify://")
        assert result is True
        mock_popen.assert_called_once_with(["cmd", "/c", "start", "", "spotify://"], shell=False)


def test_applications_launches_correct_candidate_per_platform(monkeypatch):
    monkeypatch.setattr(platform_utils, "get_os", lambda: "linux")
    # Force applications.py's module-level OS check inside launch_application
    # by monkeypatching the imported reference it actually uses.
    import execution.applications as apps_module
    monkeypatch.setattr(apps_module.platform_utils, "get_os", lambda: "linux")

    with patch.object(apps_module, "_binary_available", return_value=True), \
         patch("subprocess.Popen") as mock_popen:
        result = apps_module.launch_application("open notepad please")
        assert result is True
        mock_popen.assert_called_once_with(["gedit"])
