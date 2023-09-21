from flask import session, redirect, url_for
from datetime import datetime, timedelta, timezone
from functools import wraps
import requests
import base64
import secrets
import hashlib


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if not 'access_token' in session:
            return redirect(url_for("auth.login"))
        return function(*args, **kwargs)

    return wrapper


def encode_To_base64(string):
    string_bytes = string.encode('utf-8')
    base64_bytes = base64.b64encode(string_bytes)
    base64_string = base64_bytes.decode('utf-8')

    return base64_string


def generate_pkce_verifier_and_challenge():
    verifier = base64.urlsafe_b64encode(
        secrets.token_bytes(32)).rstrip(b"=").decode("utf-8")
    challenge = hashlib.sha256(verifier.encode("utf-8")).digest()
    challenge = base64.urlsafe_b64encode(
        challenge).rstrip(b"=").decode("utf-8")
    return verifier, challenge


def refresh_access_token(client_id):
    endpoint = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": session['refresh_token'],
        "client_id": client_id
    }

    response = requests.post(url=endpoint, headers=headers, data=data)
    json_response = response.json()

    session['access_token'] = json_response['access_token']
    session['refresh_token'] = json_response['refresh_token']
    session['token_expiry'] = datetime.now().replace(
        tzinfo=timezone.utc) + timedelta(seconds=3600)
