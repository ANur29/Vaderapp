import requests

# adressen till open meteos api
URL = "https://api.open-meteo.com/v1/forecast"


# eget fel vi kan visa för användaren
class VaderError(Exception):
    pass


# hämtar vadret just nu och tre dagars prognos för en plats
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
        # timeout så appen inte väntar för evigt om apiet inte svarar
        response = requests.get(URL, params=params, timeout=5)
        response.raise_for_status()  # ger ett fel om servern ej svarar med t.ex 404
    except requests.RequestException as fel:
        raise VaderError("Väderdata kunde inte hämtas. Försök igen") from fel

    data = response.json()
    # om det inte finns några dagar i svaret är något fel
    if not data.get("daily", {}).get("time"):
        raise VaderError("Ingen väderdata tillgänglig")
    return data
