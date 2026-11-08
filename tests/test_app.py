from unittest.mock import Mock, patch

import pytest
import requests

from application.app import app

DATA = {
    "current": {"temperature_2m": 4.2, "wind_speed_10m": 11.5},
    "daily": {
        "time": ["2026-11-01", "2026-11-02", "2026-11-03"],
        "temperature_2m_max": [6.1, 7.4, 5.0],
        "temperature_2m_min": [1.2, 2.3, -0.4],
        "precipitation_sum": [0.0, 3.2, 1.1],
    },
}


@pytest.fixture
def klient():
    app.config["TESTING"] = True
    return app.test_client()


def test_startsida(klient):
    svar = klient.get("/")
    text = svar.get_data(as_text=True)
    assert svar.status_code == 200
    assert "<select" in text
    assert "Kiruna" in text


@patch("application.api.requests.get")
def test_prognos_lyckas(mock_get, klient):
    mock_get.return_value = Mock(json=lambda: DATA)
    svar = klient.get("/prognos?stad=Umeå")
    text = svar.get_data(as_text=True)
    assert svar.status_code == 200
    assert "Väder i Umeå" in text
    assert "4,2 °C" in text
    assert "2026-11-03" in text


def test_prognos_okand_stad(klient):
    svar = klient.get("/prognos?stad=Uppsala")
    assert svar.status_code == 404
    assert "Uppsala" in svar.get_data(as_text=True)


@patch("application.api.requests.get", side_effect=requests.Timeout)
def test_prognos_timeout(mock_get, klient):
    svar = klient.get("/prognos?stad=Malmö")
    assert svar.status_code == 502
    assert "kunde inte hämtas" in svar.get_data(as_text=True)


@patch("application.api.requests.get")
def test_prognos_http_fel(mock_get, klient):
    fel_svar = Mock()
    fel_svar.raise_for_status.side_effect = requests.HTTPError("503")
    mock_get.return_value = fel_svar
    svar = klient.get("/prognos?stad=Kiruna")
    assert svar.status_code == 502


def test_egen_404_sida(klient):
    svar = klient.get("/finns-inte")
    assert svar.status_code == 404
    assert "Sidan finns inte" in svar.get_data(as_text=True)
