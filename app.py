#!/usr/bin/python3
""" Flask Application """
import json
import os
import redis
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask import session, g
from flask_session import Session
from anthropic import Anthropic
# from openai import OpenAI
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

from modules.database_utilities import db_utilities_bp
from modules.task_tracker import task_tracker_bp
from modules.task_framework import task_framework_bp


app = Flask(__name__ , static_url_path='')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key")
cors = CORS(app)

app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15) 

# app.config['SESSION_TYPE'] = 'filesystem' 

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))
Session(app)

app.register_blueprint(db_utilities_bp)
app.register_blueprint(task_tracker_bp)
app.register_blueprint(task_framework_bp)


@app.before_request
def load_session_data():
    g.environment = session.get("environment")
    # print(g.environment)
    g.interface = session.get("interface")
    g.data = session.get("data", {})
    # print(g.data)



@app.route('/interface_connections', strict_slashes=False, methods=["GET", "POST"])
def interface_connections():
    return render_template('interface_connections.html')

@app.route('/', methods=['GET'])
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

if __name__ == "__main__":
    """ Main Function """
    app.run()
