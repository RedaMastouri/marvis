#!/usr/bin/env python2
# -*-: coding utf-8 -*-
import logging
from flask import Flask, request, render_template

from snipssonos.exceptions import MusicSearchProviderConnectionError, SpotifyClientAuthorizationException, \
    SpotifyClientAuthRefreshAccessTokenException, DeviceDiscoveryException, DeezerClientAuthorizationException, \
    ConfigurationFileValidationException
from snipssonos.helpers.deezer_client import DeezerClient
from snipssonos.helpers.snips_config_parser import read_configuration_file
from snipssonos.helpers.snips_configuration_validator import validate_configuration_file
from snipssonos.helpers.spotify_client import SpotifyClient
from snipssonos.services.node.device_discovery_service import NodeDeviceDiscoveryService

CONFIG_INI = "config.ini"
# Configuration
CONFIGURATION = read_configuration_file(CONFIG_INI)

HOSTNAME = CONFIGURATION["global"].get('hostname')
CLIENT_ID = CONFIGURATION["secret"].get('client_id')
CLIENT_SECRET = CONFIGURATION["secret"].get('client_secret')
REDIRECT_URI = CONFIGURATION["secret"].get('redirect_uri')
MUSIC_PROVIDER = CONFIGURATION["global"].get('music_provider')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)


@app.route("/")
def index():
    configuration_file_errors = list()
    device_discovery_errors = list()
    devices = list()
    try:
        validate_configuration_file(CONFIGURATION)
        device_discovery_service = NodeDeviceDiscoveryService(CONFIGURATION)
        devices = device_discovery_service.get_devices()
    except ConfigurationFileValidationException as e:
        configuration_file_errors = e.message
    except DeviceDiscoveryException as e:
        device_discovery_errors = ["Could not connect to the Node SONOS API ... "]


    return render_template("index.html", client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI,
                           hostname=HOSTNAME, music_provider=MUSIC_PROVIDER, configuration_file_errors=configuration_file_errors, devices=devices, device_discovery_errors=device_discovery_errors)


@app.route("/callback/")
def authorize_callback():
    if (not CLIENT_SECRET) or (not CLIENT_ID) or not (REDIRECT_URI):
        return render_template('error.html',
                               exception="The client_id, client_secret or redirect_uri is missing from the config.ini file. Please fill these and restart the server.")

    error = request.args.get('error', None)

    if (error):  # TODO An error occured during the login phase of the user
        logging.error("An error occured when trying to log the user in")
        return "an error occured, please try again"  # Serve the adequate pages

    else:  # The application requests REFRESH and ACCESS tokens; Spotify returns access and refresh tokens
        logging.debug("Login successful. Application will request refresh and access tokens from Spotify.")

        authorization_code = request.args.get('code', None)

        try:
            access_token, refresh_token, expires_in = SpotifyClient(CLIENT_ID, CLIENT_SECRET) \
                .request_access_and_refresh_tokens(authorization_code, REDIRECT_URI)
            return render_template('auth.html', authorization_code=authorization_code,
                                   access_token=access_token,
                                   refresh_token=refresh_token,
                                   expires_in=expires_in)

        except SpotifyClientAuthorizationException as e:  # The authorization code was None
            return render_template('error.html', exception=e)

        except SpotifyClientAuthRefreshAccessTokenException as e:
            return render_template('error.html', exception=e)

        except MusicSearchProviderConnectionError as e:  # There was an error when connecting to Spotify services
            return render_template('error.html', exception=e)


@app.route('/devices/')
def get_devices():  # TODO : refactor this into a use case.
    try:
        device_discovery_service = NodeDeviceDiscoveryService(CONFIGURATION)
        devices = device_discovery_service.get_devices()
        return render_template('devices.html', devices=devices)
    except DeviceDiscoveryException as e:
        return render_template('error.html', exception=e)


@app.route("/deezer_callback/")
def deezer_authorize_callback():
    if (not CLIENT_SECRET) or (not CLIENT_ID) or not (
            REDIRECT_URI):  # There's a tight coupling with the I/O and the business logic ....
        return render_template('error.html',
                               exception="The client_id, client_secret or redirect_uri is missing from the config.ini file. Please fill these and restart the server.")

    error = request.args.get('error', None)

    if (error):  # TODO An error occured during the login phase of the user
        logging.error("An error occured when trying to log the user in")
        return "an error occured, please try again"  # Serve the adequate pages

    else:  # The application requests ACCESS token; Deezer returns access token
        logging.debug("Login successful. Application will request refresh and access tokens from Deezer.")

        authorization_code = request.args.get('code', None)

        try:
            access_token, expires_in = DeezerClient(CLIENT_ID, CLIENT_SECRET) \
                .request_access_token(authorization_code)
            return render_template('auth.html', authorization_code=authorization_code,
                                   access_token=access_token,
                                   expires_in=expires_in)

        except DeezerClientAuthorizationException as e:  # The authorization code was None
            return render_template('error.html', exception=e)

        except MusicSearchProviderConnectionError as e:  # There was an error when connecting to Spotify services
            return render_template('error.html', exception=e)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
