STADER = {
    "Stockholm": (59.33, 18.07),
    "Göteborg": (57.71, 11.97),
    "Malmö": (55.61, 13.00),
    "Umeå": (63.83, 20.26),
    "Kiruna": (67.86, 20.23),
}


def finns_stad(namn):
    return namn in STADER


def tolka_dagar(data):
    daily = data["daily"]
    dagar = []
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


def tolka_nu(data):
    current = data["current"]
    return {"temperatur": current["temperature_2m"], "vind": current["wind_speed_10m"]}


def formatera_temp(varde):
    return f"{varde:.1f} °C".replace(".", ",")
