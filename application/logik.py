STADER = {  # de fem städerna med latitud och longitud
    "Stockholm": (59.33, 18.07),
    "Göteborg": (57.71, 11.97),
    "Malmö": (55.61, 13.00),
    "Umeå": (63.83, 20.26),
    "Kiruna": (67.86, 20.23),
}


# kollar om staden finns i listan
def finns_stad(namn):
    return namn in STADER


# gör om daily listorna till en lista med en rad per dag
def tolka_dagar(data):
    daily = data["daily"]
    dagar = []
    # zip tar första värdet från varje lista, sen andra...
    for datum, hogst, lagst, nederbord in zip(
        daily["time"],
        daily["temperature_2m_max"],
        daily["temperature_2m_min"],
        daily["precipitation_sum"],
    ):
        dagar.append(
            {"datum": datum, "hogst": hogst, "lagst": lagst, "nederbord": nederbord}
        )
    return dagar


# plockar ut temperatur och vind just nu
def tolka_nu(data):
    current = data["current"]
    return {"temperatur": current["temperature_2m"], "vind": current["wind_speed_10m"]}


def formatera_temp(varde):
    return f"{varde:.1f} °C".replace(".", ",")
