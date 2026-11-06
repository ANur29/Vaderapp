from unittest.mock import Mock, patch

import pytest
import requests

from application.api import VaderError, hamta_prognos

# Ett litet påhittat svar så att testet inte behöver nätverk
DATA = {"current": {"temperature_2m": 5.0}, "daily": {"time": ["2026-11-01"]}}


# Vi patchar requests.get där den används, alltså i application.api
@patch("application.api.requests.get")
def test_hamta_prognos_lyckas(mock_get):
    mock_get.return_value = Mock(json=lambda: DATA)
    data = hamta_prognos(59.33, 18.07)
    assert data["current"]["temperature_2m"] == 5.0
    # Kollar att API:et anropades exakt en gång
    mock_get.assert_called_once()


# side_effect gör att mocken kastar ett Timeout-fel
@patch("application.api.requests.get", side_effect=requests.Timeout)
def test_hamta_prognos_timeout(mock_get):
    with pytest.raises(VaderError) as fel:
        hamta_prognos(59.33, 18.07)
    assert "kunde inte hämtas" in str(fel.value)


# raise_for_status ger ett HTTPError, som när servern svarar med 500
@patch("application.api.requests.get")
def test_hamta_prognos_http_fel(mock_get):
    svar = Mock()
    svar.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    mock_get.return_value = svar
    with pytest.raises(VaderError):
        hamta_prognos(59.33, 18.07)


# Ett svar utan dagar ska också ge vårt eget fel
@patch("application.api.requests.get")
def test_hamta_prognos_tomt_svar(mock_get):
    mock_get.return_value = Mock(json=lambda: {"daily": {"time": []}})
    with pytest.raises(VaderError):
        hamta_prognos(59.33, 18.07)
