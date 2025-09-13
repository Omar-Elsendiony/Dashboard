#!/usr/bin/python3
""" Flask Application """
import os
import redis
import requests
import json
# Third-party libraries
from flask_cors import CORS
from anthropic import Anthropic
from datetime import timedelta
from functools import lru_cache
from flask_session import Session
from oauthlib.oauth2 import WebApplicationClient
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, g
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
# Internal imports
# from modules.login_utils.db import init_db_command
from modules.login_utils.user import User
from flask_talisman import Talisman

from modules.database_utilities import db_utilities_bp
from modules.task_tracker import task_tracker_bp
from modules.task_framework import task_framework_bp
from dotenv import load_dotenv
load_dotenv()
# from modules.login import login_bp


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key")
# Talisman(app, force_https=False, strict_transport_security=True)

# CORS configuration - be more specific in production
cors = CORS(app, origins=["http://localhost:5000", "https://dashboard-omega-swart-74.vercel.app"], supports_credentials=True) 

app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) 

# app.config['SESSION_TYPE'] = 'filesystem' 

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))
Session(app)

app.register_blueprint(db_utilities_bp)
app.register_blueprint(task_tracker_bp)
app.register_blueprint(task_framework_bp)
# app.register_blueprint(login_bp)

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
    '/tasks-framework',
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

    # if not current_user.is_authenticated:
    #     if request.path not in ['/', '/login', '/login/callback', '/logout']:
    #         return redirect(url_for('index'))

######################## AUTHENTICATION WITH GOOGLE ########################

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)

# Naive database setup
# try:
#     init_db_command()
# except sqlite3.OperationalError:
#     # Assume it's already been created
#     pass

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/", strict_slashes=False)
def index():
    # if current_user.is_authenticated:
    return render_template('main.html')
    # else:
    #     return render_template('login.html')


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
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code") 
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
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
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    if not users_email.endswith("@turing.com"):
        return "Unauthorized domain", 403
    # Create a user in your db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email
    )

    # # Doesn't exist? Add it to the database.
    # if not User.get(unique_id):
    #     User.create(unique_id, users_name, users_email, picture)
    
    if not User.exists(unique_id):  # Use the new exists method
        User.create(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html')

######################## END OF OUTHENTICATION WITH GOOGLE ########################



@app.route('/interface_connections', strict_slashes=False, methods=["GET", "POST"])
def interface_connections():
    return render_template('interface_connections.html')

@app.route('/index', strict_slashes=False, methods=['GET'])
def home_page():
    return render_template('main.html')


def get_claude_client():
    """Initialize and return Claude client"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return Anthropic(api_key=api_key)

# Helper function to call Claude
def call_claude(prompt, model="claude-3-5-sonnet-20241022", max_tokens=4000, temperature=0.1):
    """
    Call Claude API with the given prompt
    
    Args:
        prompt (str): The prompt to send to Claude
        model (str): Claude model to use (default: claude-3-5-sonnet-20241022)
        max_tokens (int): Maximum tokens to generate
        temperature (float): Temperature for response generation
    
    Returns:
        str: Claude's response content
    """
    client = get_claude_client()
    
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.content[0].text


@app.route('/instruction_validation', strict_slashes=False, methods=["GET", "POST"])
def instruction_validation():
    if request.method == "POST":
        data = request.json
        action = data.get('action')
        if not action:
            return jsonify({
                'status': 'error',
                'message': 'Action is required'
            }), 400
        
        if action == "fetch_initial_prompt":
            initial_prompt_file_path = f"prompts/instruction_validator/initial_prompt.txt"
            if not os.path.exists(initial_prompt_file_path):
                return jsonify({
                    'status': 'error',
                    'message': f'Initial prompt file for {action} not found'
                }), 404
            
            with open(initial_prompt_file_path, 'r') as file:
                initial_prompt = file.read()
            
            examples_file_path = f"prompts/instruction_validator/examples.txt"
            with open(examples_file_path, 'r') as file:
                examples = file.read()
            
            return jsonify({
                'status': 'success',
                'initial_prompt': initial_prompt,
                'examples': examples
            }), 200
        
        elif action == "validate_instruction":
            initial_prompt = data.get('initial_prompt', '')
            examples = data.get('examples', '')
            policy = data.get('policy', '')
            instruction = data.get('instruction', '')
            model = data.get('model', '')
            
            if not initial_prompt or not policy:
                return jsonify({
                    'status': 'error',
                    'message': 'Initial prompt and policy are required'
                }), 400
            
            
            prompt = initial_prompt.format(
                policy=policy,
                instruction=instruction,
                examples=examples if examples else ""
            )
            
            # from openai import OpenAI
            # client = OpenAI() 
            
            try:
                # response = client.chat.completions.create(
                #     model=model,
                #     messages=[
                #         {"role": "system", "content": "You are a helpful assistant."},
                #         {"role": "user", "content": prompt}
                #     ],
                #     temperature=0.1
                # )
                
                # validation_result = response.choices[0].message.content.strip()
                
                validation_result = call_claude(prompt, model=model)

                return jsonify({
                    'status': 'success',
                    'validation_result': validation_result
                }), 200
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': f'Failed to validate instruction: {str(e)}'
                }), 500
        else:
            return jsonify({
                'status': 'error',
                'message': 'Invalid action'
            }), 400

    return render_template('instruction_validation.html')

@app.route('/instruction_relevant_actions_or_policies', strict_slashes=False, methods=["GET", "POST"])
def instruction_relevant_actions_or_policies():
    if request.method == "POST":
        data = request.json
        instruction = data.get('instruction', '')
        model = data.get('model', '')

        if not instruction:
            return jsonify({
                'status': 'error',
                'message': 'Instruction is required'
            }), 400

        prompt = f"Extract relevant actions and policies from the following instruction:\n\n{instruction}"

        try:
            validation_result = call_claude(prompt, model=model)

            return jsonify({
                'status': 'success',
                'validation_result': validation_result
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to extract actions or policies: {str(e)}'
            }), 500
    else:
        return render_template('instruction_relevant_actions_or_policies.html')

# Add this route to your Flask app
@app.route('/google0798b17d9d33abf1.html')  # Replace with your actual filename
def google_verification():
    return 'google-site-verification: google0798b17d9d33abf1.html'  # Replace with actual content

if __name__ == "__main__":
    """ Main Function """
    # app.run(ssl_context="adhoc")
    app.run()
