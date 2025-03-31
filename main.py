from flask import Flask, render_template, redirect, url_for, session, request
from flask_pymongo import PyMongo
from oauthlib.oauth2 import WebApplicationClient
import requests
from config import Config
import os  # Add this import

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB setup
mongo = PyMongo(app)

# Google OAuth setup
client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    google_provider_cfg = requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=url_for('callback', _external=True),
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route('/callback')
def callback():
    code = request.args.get("code")
    google_provider_cfg = requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=url_for('callback', _external=True),
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
    )
    client.parse_request_body_response(token_response.text)
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    user_info = userinfo_response.json()

    # Store user info in MongoDB
    user = mongo.db.users.find_one({"email": user_info["email"]})
    if not user:
        mongo.db.users.insert_one({
            "email": user_info["email"],
            "name": user_info["name"],
            "picture": user_info["picture"]
        })
    session['user'] = user_info
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', user=session['user'])

if __name__ == '__main__':
    app.secret_key = app.config['SECRET_KEY']
    
    # Allow insecure transport for development purposes
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    app.run(debug=True)
