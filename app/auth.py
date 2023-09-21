from flask import Blueprint, request, redirect, session, url_for, abort
from dotenv import load_dotenv
from app.utils import generate_pkce_verifier_and_challenge, encode_To_base64, login_required
from datetime import datetime, timedelta, timezone
import requests
import urllib.parse
import os

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPE = "user-read-private user-read-email user-follow-read user-top-read playlist-read-private"

auth = Blueprint("auth", __name__)


@auth.route('/login', methods=['GET'])
def login():
    if not 'access_token' in session:
        pkce_verifier, pkce_challenge = generate_pkce_verifier_and_challenge()
        session['pkce_verifier'] = pkce_verifier

        auth_params = {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPE,
            "code_challenge_method": "S256",
            "code_challenge": pkce_challenge
        }

        url = f"{AUTH_URL}?{urllib.parse.urlencode(auth_params)}"

        session['callback_referrer'] = url

        return redirect(url)

    return redirect(url_for("routes.get_profile"))


@auth.route('/callback', methods=['GET'])
def callback():
    if not 'callback_referrer' in session:
        abort(404)

    auth_code = request.args.get("code")
    auth_header = encode_To_base64(f'{CLIENT_ID}:{CLIENT_SECRET}')

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": session['pkce_verifier']
    }

    response = requests.post(url=TOKEN_URL, headers=headers, data=data)
    json_response = response.json()

    session['access_token'] = json_response['access_token']
    session['refresh_token'] = json_response['refresh_token']
    session['token_expiry'] = datetime.now().replace(
        tzinfo=timezone.utc) + timedelta(seconds=3600)

    session.pop('callback_referrer', None)

    return redirect(url_for('routes.get_profile')), 200


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()

    return {"message": "You are logged out"}
