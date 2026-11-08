import pytest

from application.logik import finns_stad, formatera_temp, tolka_dagar, tolka_nu


# skrev testet innan funktionen fanns
@pytest.mark.parametrize(
    "namn, forvantat",
    [
        ("Stockholm", True),
        ("Kiruna", True),
        ("Göteborg", True),
        ("Uppsala", False),
        ("stockholm", False),
        ("", False),
        (None, False),
    ],
)
def test_finns_stad(namn, forvantat):
    assert finns_stad(namn) == forvantat


# påhittad data som ser ut som svar från apiet
DATA = {
    "current": {"temperature_2m": 4.2, "wind_speed_10m": 11.5},
    "daily": {
        "time": ["2026-11-01", "2026-11-02", "2026-11-03"],
        "temperature_2m_max": [6.1, 7.4, 5.0],
        "temperature_2m_min": [1.2, 2.3, -0.4],
        "precipitation_sum": [0.0, 3.2, 1.1],
    },
}


# kollar att varje dag får rätt värden
@pytest.mark.parametrize(
    "index, forvantat",
    [
        (0, {"datum": "2026-11-01", "hogst": 6.1, "lagst": 1.2, "nederbord": 0.0}),
        (1, {"datum": "2026-11-02", "hogst": 7.4, "lagst": 2.3, "nederbord": 3.2}),
        (2, {"datum": "2026-11-03", "hogst": 5.0, "lagst": -0.4, "nederbord": 1.1}),
    ],
)
def test_tolka_dagar(index, forvantat):
    dagar = tolka_dagar(DATA)
    assert len(dagar) == 3
    assert dagar[index] == forvantat


def test_tolka_nu():
    assert tolka_nu(DATA) == {"temperatur": 4.2, "vind": 11.5}


# kollar avrundning, minusgrader och decimalkomma
@pytest.mark.parametrize(
    "varde, forvantat",
    [
        (12.34, "12,3 °C"),
        (0, "0,0 °C"),
        (-5.06, "-5,1 °C"),
        (20, "20,0 °C"),
    ],
)
def test_formatera_temp(varde, forvantat):
    assert formatera_temp(varde) == forvantat
