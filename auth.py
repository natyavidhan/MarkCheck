from flask import Blueprint, redirect, url_for, session, request
from flask_pymongo import PyMongo
from oauthlib.oauth2 import WebApplicationClient
import requests
from config import Config

auth_bp = Blueprint('auth', __name__)

client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)

@auth_bp.route('/login')
def login():
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('auth.callback', _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth_bp.route('/callback')
def callback():
    code = request.args.get("code")
    google_provider_cfg = requests.get(Config.GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for('auth.callback', _external=True),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET),
    )
    client.parse_request_body_response(token_response.text)
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    user_info = userinfo_response.json()

    # Store user info in MongoDB
    user = auth_bp.mongo.db.users.find_one({"email": user_info["email"]})
    if not user:
        auth_bp.mongo.db.users.insert_one({
            "email": user_info["email"],
            "name": user_info["name"],
            "picture": user_info["picture"],
            "boards": []
        })
    session['user'] = user_info['email']
    return redirect(url_for('index'))

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))
