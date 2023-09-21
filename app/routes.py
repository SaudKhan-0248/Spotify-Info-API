from flask import Blueprint, session
from app.utils import login_required
from datetime import datetime, timezone
from app import utils
import requests
import os

routes = Blueprint("routes", __name__)


@routes.before_request
@login_required
def before_request():
    if datetime.now().replace(tzinfo=timezone.utc) >= session['token_expiry']:
        utils.refresh_access_token(os.getenv('CLIENT_ID'))


@routes.route('/profile', methods=['GET'])
def get_profile():
    access_token = session['access_token']

    endpoint = "https://api.spotify.com/v1/me"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url=endpoint, headers=headers)
    json_resp = response.json()

    spotify_id = json_resp['id']
    name = json_resp['display_name']
    email = json_resp['email']
    subscription = json_resp['product']
    followers = json_resp['followers']['total']

    return {"name": name, "email": email, "spotify_id": spotify_id, "subscription": subscription, "followers": followers}


@routes.route('/artists/followed', methods=['GET'])
def get_followed_artists():
    access_token = session['access_token']

    endpoint = "https://api.spotify.com/v1/me/following?type=artist"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {}
    artist_names = list()

    while True:
        response = requests.get(url=endpoint, headers=headers, params=params)
        json_response = response.json()

        names = [artist['name']
                 for artist in json_response['artists']['items']]

        artist_ids = [artist['id']
                      for artist in json_response['artists']['items']]

        artist_names.extend(names)
        last_id = artist_ids[-1]

        if not json_response['artists']['next']:
            break

        params = {
            "after": last_id
        }

    return {"Artists you Follow": artist_names}


@routes.route('/playlists/followed', methods=['GET'])
def get_playlists():
    access_token = session['access_token']

    endpoint = "https://api.spotify.com/v1/me/playlists"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url=endpoint, headers=headers)
    json_response = response.json()

    playlist_names = [field['name'] for field in json_response['items']]

    return {"Playlists you Follow or Own": playlist_names}


@routes.route('/tracks/top', methods=['GET'])
def get_top_tracks():
    access_token = session['access_token']

    endpoint = "https://api.spotify.com/v1/me/top/tracks"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url=endpoint, headers=headers)
    json_response = response.json()

    track_names = [field['name'] for field in json_response['items']]

    return {"Your top 20 Tracks": track_names}


@routes.route('/artists/top', methods=['GET'])
def get_top_artists():
    access_token = session['access_token']

    endpoint = "https://api.spotify.com/v1/me/top/artists"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url=endpoint, headers=headers)
    json_response = response.json()

    artist_names = [artist['name'] for artist in json_response['items']]

    return {"Your top 20 Artists": artist_names}
