#!/usr/bin/python3
""" Flask Application - Optimized Version """
import os
import redis
import requests
import json
from functools import lru_cache
from datetime import timedelta

# Third-party libraries
from flask_cors import CORS
from anthropic import Anthropic
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
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

# Internal imports
from modules.login_utils.user import User
from modules.database_utilities import db_utilities_bp
from modules.task_tracker import task_tracker_bp
from modules.task_framework import task_framework_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Security configurations
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key")

# Add security headers with Talisman
Talisman(app, force_https=False, strict_transport_security=True)

# CORS configuration - be more specific in production
cors = CORS(app, origins=["https://dashboard-omega-swart-74.vercel.app"])
# Rate limiting
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Session configuration
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
app.config['SESSION_TYPE'] = 'redis'

# Redis configuration with connection pooling
redis_url = os.environ.get('REDIS_URL')
if redis_url:
    app.config['SESSION_REDIS'] = redis.ConnectionPool.from_url(
        redis_url, 
        max_connections=20,
        retry_on_timeout=True,
        socket_connect_timeout=5,
        socket_timeout=5
    )
    app.config['SESSION_REDIS'] = redis.Redis(connection_pool=app.config['SESSION_REDIS'])
else:
    # Fallback to filesystem sessions in development
    app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

# Register blueprints
app.register_blueprint(db_utilities_bp)
app.register_blueprint(task_tracker_bp)
app.register_blueprint(task_framework_bp)

# Route configurations
PUBLIC_ROUTES = {
    '/',
    '/login',
    '/login/callback',
    '/logout',
    '/static',
    '/google0798b17d9d33abf1.html'
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
    """Optimized session data loading"""
    try:
        g.environment = session.get("environment")
        g.interface = session.get("interface")
        g.data = session.get("data", {})
        
        # Skip authentication for static files and public routes
        if (request.path.startswith('/static/') or 
            request.path in PUBLIC_ROUTES or 
            'google' in request.path):
            return

        # Redirect unauthenticated users for protected routes
        if request.path in REDIRECT_ROUTES and not current_user.is_authenticated:
            return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f"Error in before_request: {e}")
        return jsonify({'error': 'Session error'}), 500

######################## AUTHENTICATION WITH GOOGLE ########################

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("Google OAuth credentials are required")

# User session management
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

@login_manager.user_loader
def load_user(user_id):
    """Load user with error handling"""
    try:
        return User.get(user_id)
    except Exception as e:
        app.logger.error(f"Error loading user {user_id}: {e}")
        return None

@app.route("/", strict_slashes=False)
def index():
    if current_user.is_authenticated:
        return render_template('main.html')
    else:
        return render_template('login.html')

@lru_cache(maxsize=1)
def get_google_provider_cfg():
    """Cached Google provider configuration with error handling"""
    try:
        response = requests.get(GOOGLE_DISCOVERY_URL, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        app.logger.error(f"Failed to get Google provider config: {e}")
        return None

@app.route("/login")
@limiter.limit("10 per minute")
def login():
    """Rate-limited login endpoint"""
    try:
        google_provider_cfg = get_google_provider_cfg()
        if not google_provider_cfg:
            return jsonify({'error': 'Authentication service unavailable'}), 503
            
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return redirect(request_uri)
    except Exception as e:
        app.logger.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500

@app.route("/login/callback")
@limiter.limit("5 per minute")
def callback():
    """Rate-limited callback endpoint with improved error handling"""
    try:
        code = request.args.get("code")
        if not code:
            return "Authorization code missing", 400
            
        google_provider_cfg = get_google_provider_cfg()
        if not google_provider_cfg:
            return "Authentication service unavailable", 503
            
        token_endpoint = google_provider_cfg["token_endpoint"]
        
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
            timeout=10
        )
        token_response.raise_for_status()

        client.parse_request_body_response(json.dumps(token_response.json()))
        
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body, timeout=10)
        userinfo_response.raise_for_status()
        
        userinfo = userinfo_response.json()
        
        if not userinfo.get("email_verified"):
            return "Email not verified by Google", 400

        unique_id = userinfo["sub"]
        users_email = userinfo["email"]
        users_name = userinfo["given_name"]
        
        # Domain validation
        if not users_email.endswith("@turing.com"):
            return "Unauthorized domain", 403

        # Create or get user
        user = User(id_=unique_id, name=users_name, email=users_email)
        
        if not User.exists(unique_id):
            if not User.create(unique_id, users_name, users_email):
                return "Failed to create user", 500

        login_user(user)
        return redirect(url_for("index"))
        
    except requests.RequestException as e:
        app.logger.error(f"HTTP error in callback: {e}")
        return "Authentication service error", 503
    except Exception as e:
        app.logger.error(f"Callback error: {e}")
        return "Authentication failed", 500

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return render_template('login.html')

######################## END OF AUTHENTICATION WITH GOOGLE ########################

@app.route('/interface_connections', strict_slashes=False, methods=["GET", "POST"])
@login_required
def interface_connections():
    return render_template('interface_connections.html')

@app.route('/index', strict_slashes=False, methods=['GET'])
@login_required
def home_page():
    return render_template('main.html')

# Claude client with connection pooling
@lru_cache(maxsize=1)
def get_claude_client():
    """Cached Claude client initialization"""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return Anthropic(api_key=api_key)

def call_claude(prompt, model="claude-3-5-sonnet-20241022", max_tokens=4000, temperature=0.1):
    """
    Optimized Claude API call with error handling and timeouts
    """
    try:
        client = get_claude_client()
        
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
            timeout=30.0  # Add timeout
        )
        
        return response.content[0].text
    except Exception as e:
        app.logger.error(f"Claude API error: {e}")
        raise

@app.route('/instruction_validation', strict_slashes=False, methods=["GET", "POST"])
@login_required
@limiter.limit("20 per minute")
def instruction_validation():
    if request.method == "POST":
        try:
            data = request.json
            if not data:
                return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400
                
            action = data.get('action')
            if not action:
                return jsonify({'status': 'error', 'message': 'Action is required'}), 400
            
            if action == "fetch_initial_prompt":
                initial_prompt_file_path = "prompts/instruction_validator/initial_prompt.txt"
                examples_file_path = "prompts/instruction_validator/examples.txt"
                
                if not os.path.exists(initial_prompt_file_path):
                    return jsonify({
                        'status': 'error',
                        'message': 'Initial prompt file not found'
                    }), 404
                
                try:
                    with open(initial_prompt_file_path, 'r', encoding='utf-8') as file:
                        initial_prompt = file.read()
                    
                    examples = ""
                    if os.path.exists(examples_file_path):
                        with open(examples_file_path, 'r', encoding='utf-8') as file:
                            examples = file.read()
                    
                    return jsonify({
                        'status': 'success',
                        'initial_prompt': initial_prompt,
                        'examples': examples
                    })
                except IOError as e:
                    app.logger.error(f"File read error: {e}")
                    return jsonify({'status': 'error', 'message': 'File read error'}), 500
            
            elif action == "validate_instruction":
                required_fields = ['initial_prompt', 'policy']
                missing_fields = [field for field in required_fields if not data.get(field)]
                
                if missing_fields:
                    return jsonify({
                        'status': 'error',
                        'message': f'Missing required fields: {", ".join(missing_fields)}'
                    }), 400
                
                initial_prompt = data['initial_prompt']
                examples = data.get('examples', '')
                policy = data['policy']
                instruction = data.get('instruction', '')
                model = data.get('model', 'claude-3-5-sonnet-20241022')
                
                prompt = initial_prompt.format(
                    policy=policy,
                    instruction=instruction,
                    examples=examples
                )
                
                try:
                    validation_result = call_claude(prompt, model=model)
                    return jsonify({
                        'status': 'success',
                        'validation_result': validation_result
                    })
                except Exception as e:
                    app.logger.error(f"Claude validation error: {e}")
                    return jsonify({
                        'status': 'error',
                        'message': 'Validation service temporarily unavailable'
                    }), 503
            else:
                return jsonify({'status': 'error', 'message': 'Invalid action'}), 400
                
        except Exception as e:
            app.logger.error(f"Validation endpoint error: {e}")
            return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

    return render_template('instruction_validation.html')

@app.route('/instruction_relevant_actions_or_policies', strict_slashes=False, methods=["GET", "POST"])
@login_required
@limiter.limit("20 per minute")
def instruction_relevant_actions_or_policies():
    if request.method == "POST":
        try:
            data = request.json
            if not data:
                return jsonify({'status': 'error', 'message': 'Invalid JSON'}), 400
                
            instruction = data.get('instruction', '').strip()
            model = data.get('model', 'claude-3-5-sonnet-20241022')

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
                })
            except Exception as e:
                app.logger.error(f"Policy extraction error: {e}")
                return jsonify({
                    'status': 'error',
                    'message': 'Service temporarily unavailable'
                }), 503
                
        except Exception as e:
            app.logger.error(f"Policy endpoint error: {e}")
            return jsonify({'status': 'error', 'message': 'Internal server error'}), 500
    else:
        return render_template('instruction_relevant_actions_or_policies.html')

@app.route('/google0798b17d9d33abf1.html')
def google_verification():
    return 'google-site-verification: google0798b17d9d33abf1.html'

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal error: {error}")
    return render_template('error.html', error="Internal server error"), 500

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

if __name__ == "__main__":
    # Production-ready configuration
    app.run()
    # port = int(os.environ.get('PORT', 5000))
    # debug = os.environ.get('FLASK_ENV') == 'development'
    
    # if debug:
    #     app.run(debug=True, port=port)
    # else:
    #     # Use a production WSGI server like Gunicorn in production
    #     app.run(host='0.0.0.0', port=port, debug=False)