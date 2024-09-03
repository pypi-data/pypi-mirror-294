
from flask import session, request, current_app
from dataclasses import dataclass
from typing import Optional
import geoip2.database
import os
import click
import sys
import subprocess


DOWNLOAD_URL = "https://download.maxmind.com/app/geoip_download"
COUNTRY_EDITION = "GeoLite2-Country"
CITY_EDITION = "GeoLite2-City"


@dataclass
class GeolocationState:
    maxmind_db: str
    is_city_db: bool
    silent: bool
    reader: Optional[geoip2.database.Reader] = None


class GeolocationError(Exception):
    pass


class Geolocation:
    def __init__(self, app=None, **kwargs):
        if app:
            self.init_app(app, **kwargs)
    
    def init_app(self, app, maxmind_db="GeoLite2-City.mmdb", is_city_db=True, silent=True):
        app.jinja_env.globals.update(
            geolocate_country=geolocate_country,
            geolocate_city=geolocate_city
        )

        maxmind_db = app.config.get("FLASK_GEO_MAXMIND_DB", maxmind_db)
        state = app.extensions["flask_geo"] = GeolocationState(
            maxmind_db=maxmind_db,
            is_city_db=app.config.get("FLASK_GEO_USE_CITY_DB", is_city_db),
            silent=app.config.get("FLASK_GEO_SILENT", silent)
        )

        if os.path.exists(maxmind_db):
            state.reader = geoip2.database.Reader(maxmind_db)
        elif not silent:
            raise GeolocationError("Missing maxmind db file")
        else:
            app.logger.info("No maxmind db file found, geolocation is disabled")

        @app.cli.command('download-geo-db')
        @click.option('--edition')
        @click.option('--suffix', default='tar.gz')
        @click.option('--license-key')
        def download_db(edition=None, suffix='tar.gz', license_key=None):
            """Download GeoLite2 databases from MaxMind"""
            if not license_key:
                click.echo("You must register on MaxMind to obtain a license key in order to download databases")
                sys.exit(1)
            tmpfilename = "/tmp/GeoLite2.tar.gz"
            if not edition:
                edition = CITY_EDITION if state.is_city_db else COUNTRY_EDITION
            url = "%s?edition_id=%s&suffix=%s&license_key=%s" % (DOWNLOAD_URL, edition, suffix, license_key)
            subprocess.run(["wget", "-O", tmpfilename, url])
            dbfilename = subprocess.run(["tar", "tzf", tmpfilename, "--no-anchored", state.maxmind_db], capture_output=True, text=True).stdout.strip()
            subprocess.run(["tar", "-C", "/tmp", "-xzf", tmpfilename, dbfilename])
            subprocess.run(["mv", os.path.join("/tmp", dbfilename), state.maxmind_db])


def geolocate(remote_addr=None, method=None):
    state = current_app.extensions["flask_geo"]
    if not state.reader:
        return
    if not method:
        method = 'city' if state.is_city_db else 'country'

    if not remote_addr:
        remote_addr = request.remote_addr
        if current_app.debug and "__remoteaddr" in request.values:
            remote_addr = request.values["__remoteaddr"]

    try:
        return getattr(state.reader, method)(remote_addr)
    except:
        if not state.silent:
            raise GeolocationError()


def geolocate_country(remote_addr=None, use_session_cache=True):
    if use_session_cache and current_app.secret_key and "geo_country_code" in session:
        return session["geo_country_code"]

    if current_app.extensions["flask_geo"].is_city_db:
        city, country = geolocate_city(remote_addr, use_session_cache)
        return country

    r = geolocate(remote_addr, 'country')
    if r:
        if use_session_cache and current_app.secret_key:
            session["geo_country_code"] = r.country.iso_code
        return r.country.iso_code


def geolocate_city(remote_addr=None, use_session_cache=True):
    if use_session_cache and current_app.secret_key and "geo_city" in session:
        return session["geo_city"]
    r = geolocate(remote_addr, 'city')
    if r:
        if use_session_cache and current_app.secret_key:
            session["geo_city"] = r.city.name
            session["geo_country_code"] = r.country.iso_code
        return r.city.name, r.country.iso_code
    return None, None


def clear_geo_cache():
    session.pop("geo_country_code", None)
    session.pop("geo_city", None)
