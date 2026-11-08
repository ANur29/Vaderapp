import requests
# första testet mot api:et för att se hur svaret ser ut
params = {
    "latitude": 59.33,
    "longitude": 18.07,
    "current": "temperature_2m,wind_speed_10m",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "auto",
    "forecast_days": 3,
}
svar = requests.get("https://api.open-meteo.com/v1/forecast", params=params, timeout=5)
data = svar.json()
# skriver ut nycklarna och värdena så jag ser vad som finns
print(data.keys())
print(data["current"])
print(data["daily"])
