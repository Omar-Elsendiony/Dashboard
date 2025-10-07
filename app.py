#!/usr/bin/python3
""" Flask Application """
import os
import redis
import requests
import json
# Third-party libraries
from flask_cors import CORS
from datetime import timedelta
from functools import lru_cache
from flask_session import Session
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, render_template, request, redirect, url_for, session, g
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from modules.login_utils.user import User
# from flask_talisman import Talisman

################# BLUEPRINTS #####################
from modules.database_utilities import db_utilities_bp
from modules.task_tracker import task_tracker_bp
from modules.task_framework import task_framework_bp
from modules.instruction_validation import instruction_validation_bp
from modules.interface_connections import interface_connections_bp
################# END OF BLUEPRINTS #####################

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY environment variable must be set")

# Talisman(app, 
#     force_https=True,
#     strict_transport_security=True,
#     content_security_policy={
#         'default-src': "'self'",
#         'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
#         'style-src': "'self' 'unsafe-inline'",
#         'img-src': "'self' data: https:",
#         'font-src': "'self' https:",
#         'connect-src': "'self' https:",
#         'frame-src': "'none'",
#         'object-src': "'none'",
#         'base-uri': "'self'"
#     }
# )

# CORS configuration
cors = CORS(app) 

app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) 

# app.config['SESSION_TYPE'] = 'filesystem' 

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))
Session(app)

########### REGISTER BLUEPRINTS ###########
app.register_blueprint(db_utilities_bp)
app.register_blueprint(task_tracker_bp)
app.register_blueprint(task_framework_bp)
app.register_blueprint(instruction_validation_bp)
app.register_blueprint(interface_connections_bp)
######### END OF REGISTER BLUEPRINTS #########

PUBLIC_ROUTES = {
    '/',
    '/login',
    '/login/callback',
    '/logout',
    '/static',
}

REDIRECT_ROUTES = {
    '/interface_connections',
    '/instruction_validation',
    '/instruction_relevant_actions_or_policies',
    '/index',
    '/tracker',
    '/task-framework',
    '/db_utilities'
}

@app.before_request
def load_session_data():
    g.environment = session.get("environment")
    g.interface = session.get("interface")
    g.data = session.get("data", {})
    
    if request.path.startswith('/static/') or request.path in ['static'] or request.path in PUBLIC_ROUTES or 'google' in request.path:
        return

    if request.path in REDIRECT_ROUTES and not current_user.is_authenticated:
        return redirect(url_for('index'))

######################## AUTHENTICATION WITH GOOGLE ########################

# Configuration
def get_oauth_config():
    """Get OAuth configuration based on current request host"""
    if "dashboard-omega-swart-74.vercel.app" in request.host:
        client_id = os.environ.get("GOOGLE_CLIENT_ID")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    else:
        client_id = os.environ.get("GOOGLE_CLIENT_ID_2")
        client_secret = os.environ.get("GOOGLE_CLIENT_SECRET_2")
    
    if not client_id or not client_secret:
        raise ValueError("OAuth credentials not configured properly")
    
    return client_id, client_secret

GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/", strict_slashes=False)
def index():
    if current_user.is_authenticated:
        return render_template('main.html')
    else:
        return render_template('login.html')




@lru_cache(maxsize=1)
def get_google_provider_cfg():
    try:
        response = requests.get(GOOGLE_DISCOVERY_URL, timeout=5)
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to get Google provider config: {e}")
        return None

@app.route("/login")
def login():
    try:
        # Get OAuth config for current host
        client_id, client_secret = get_oauth_config()
        
        # Create client with proper credentials
        client = WebApplicationClient(client_id)
        
        # Find out what URL to hit for Google login
        google_provider_cfg = get_google_provider_cfg()
        if not google_provider_cfg:
            return "OAuth configuration failed", 500
            
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login
        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)
    except Exception as e:
        print(f"Login error: {e}")
        return f"OAuth configuration error: {e}", 500

@app.route("/login/callback")
def callback():
    try:
        # Get OAuth config for current host
        client_id, client_secret = get_oauth_config()
        
        # Create client with proper credentials
        client = WebApplicationClient(client_id)
        
        # Get authorization code Google sent back
        code = request.args.get("code")
        if not code:
            return "Authorization code not received", 400
            
        # Get provider configuration
        google_provider_cfg = get_google_provider_cfg()
        if not google_provider_cfg:
            return "OAuth configuration failed", 500
            
        token_endpoint = google_provider_cfg["token_endpoint"]
        
        # Prepare and send request to get tokens
        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(client_id, client_secret),
            timeout=10
        )

        if not token_response.ok:
            return f"Token request failed: {token_response.text}", 400

        # Parse the tokens
        client.parse_request_body_response(json.dumps(token_response.json()))
        
        # Get user info
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body, timeout=10)

        if not userinfo_response.ok:
            return f"User info request failed: {userinfo_response.text}", 400

        user_info = userinfo_response.json()
        
        # Verify email
        if not user_info.get("email_verified"):
            return "User email not available or not verified by Google.", 400

        # Check domain restriction
        users_email = user_info["email"]
        if not users_email.endswith("@turing.com"):
            return "Unauthorized domain", 403

        # Create user
        unique_id = user_info["sub"]
        users_name = user_info["given_name"]
        
        user = User(id_=unique_id, name=users_name, email=users_email)

        if not User.exists(unique_id):
            User.create(unique_id, users_name, users_email)

        # Login user
        login_user(user)
        return redirect(url_for("index"))
        
    except Exception as e:
        print(f"Callback error: {e}")
        return f"Authentication error: {e}", 500

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html')

######################## END OF OUTHENTICATION WITH GOOGLE ########################

@app.route('/index', strict_slashes=False, methods=['GET'])
def home_page():
    return render_template('main.html')


if __name__ == "__main__":
    """ Main Function """
    app.run()
