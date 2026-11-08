# Väderappen

En Flask-app där man väljer en stad och ser vädret just nu och en prognos för tre dagar.
Datan hämtas från Open-Meteo.

## Installation

Klona projektet och gå in i mappen:

```bash
git clone https://github.com/ANur29/Vaderapp.git
cd Vaderapp
```

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

## Starta appen

```powershell
python -m flask --app application.app run
```

Öppna http://127.0.0.1:5000 i webbläsaren.

## Tester och ruff

```powershell
python -m pytest
python -m ruff check .
python -m ruff format --check .
```

På Mac används `python3` istället för `python`.

## Frågor

### 1. Varför mockar du anropen mot API:et?

Jag mockar requests.get med @patch så att testerna får påhittad data istället för att hämta från internet. Då ger testerna samma resultat varje gång och jag kan låtsas att API:et får timeout eller fel. Utan mockning skulle testerna gå sönder om internet är nere eller om vädret ändras.

### 2. Vad gör timeout och raise_for_status()?

timeout=5 gör att anropet ger upp efter 5 sekunder så att appen inte väntar för evigt. raise_for_status() ger ett fel om servern svarar med en felkod som 404 eller 500. I api.py gör jag om felen till VaderError så att appen visar ett felmeddelande istället för att krascha.

### 3. Hur fungerar mallarv i Jinja2?

base.html har det som är samma på alla sidor, som navbaren och källan, och blocken title och content. De andra mallarna börjar med {% extends "base.html" %} och fyller bara i sina egna block, till exempel lägger prognos.html tabellen i content. Då behöver jag bara skriva den gemensamma koden en gång.

### 4. Vad är en fixture, och vilken använder du?

En fixture är en funktion med @pytest.fixture som förbereder något som flera tester behöver.
Jag använder fixturen klient i test_app.py som ger en testklient så att testerna kan besöka sidorna utan att starta servern.

## API och källa

Jag använder Open-Meteo Weather Forecast API, som inte behöver någon API-nyckel.

Dokumentation: https://open-meteo.com/en/docs

Datakälla: https://open-meteo.com/ (CC BY 4.0)