import requests

URL = "https://api.open-meteo.com/v1/forecast"


class VaderError(Exception):
    pass


def hamta_prognos(latitud, longitud):
    params = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,wind_speed_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto",
        "forecast_days": 3,
    }

    try:
        response = requests.get(URL, params=params, timeout=5)
        response.raise_for_status()
    except requests.RequestException as fel:
        raise VaderError("Väderdata kunde inte hämtas. Försök igen") from fel

    data = response.json()

    if not data.get("daily", {}).get("time"):
        raise VaderError("Ingen väderdata tillgänglig")
    return data
