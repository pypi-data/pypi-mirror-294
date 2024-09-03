# Flask-Geo

Geolocation for Flask using Maxmind.

## Installation

    pip install flask-geo

## Usage

Initialize the extension:

```python
from flask import Flask
from flask_geo import Geolocation

app = Flask(__name__)
geo = Geolocation(app)
```

Download a maxmind db:

    flask download-geo-db --license-key=XXX

Get the country or city of the visitor:

```python
from flask_geo import geolocate_country, geolocate_city

@app.route("/")
def index():
    country_iso_code = geolocate_country()
    # or
    city_name, country_iso_code = geolocate_city()
```

> [!IMPORTANT]
> Geolocation results are cached in the session. To clear the cache use `clear_geo_cache()`

> [!TIP]
> When app.debug is true, you can override which ip address to use for geolocation using the `__remoteaddr` query parameter: `http://localhost:5000?__remoteaddr=1.1.1.1`

## Configuration

| Config key | Extension argument | Description | Default |
| --- | --- | --- | --- |
| FLASK_GEO_MAXMIND_DB | maxmind_db | Filename towards the maxmind db | GeoLite2-City.mmdb |
| FLASK_GEO_USE_CITY_DB | is_city_db | Whether it is the city db or the country db | True |
| FLASK_GEO_SILENT | silent | Do not raise any errors whether the db is missing or geolocation fails | True |