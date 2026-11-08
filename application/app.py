from flask import Flask, render_template, request

from application.api import VaderError, hamta_prognos
from application.logik import (
    STADER,
    finns_stad,
    formatera_temp,
    tolka_dagar,
    tolka_nu,
)

app = Flask(__name__)
# gör formatera_temp till en filter som heter temp i mallarna
app.add_template_filter(formatera_temp, "temp")


# startsidan med listan över städer
@app.route("/")
def index():
    return render_template("index.html", stader=STADER)


# prognossidan, staden kommer från adressen
@app.route("/prognos")
def prognos():
    stad = request.args.get("stad")

    if not finns_stad(stad):
        return render_template("fel.html", fel=f"Staden '{stad}' finns inte."), 404

    latitud, longitud = STADER[stad]
    try:
        data = hamta_prognos(latitud, longitud)
    except VaderError as fel:
        return render_template("fel.html", fel=str(fel)), 502

    return render_template(
        "prognos.html", stad=stad, nu=tolka_nu(data), dagar=tolka_dagar(data)
    )


# sida när adressen inte fins
@app.errorhandler(404)
def sidan_finns_inte(e):
    return render_template("fel.html", fel="Sidan finns inte."), 404


if __name__ == "__main__":
    app.run(debug=True)
