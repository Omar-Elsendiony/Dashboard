#!/usr/bin/python3
""" Flask Application """
import json
import os
import redis
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from flask import session, g
from flask_session import Session
# from openai import OpenAIcd 
from anthropic import Anthropic
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from datetime import timedelta
from task_framework_utils import extract_file_info, create_tools_class, arguments_processing
from dotenv import load_dotenv
load_dotenv()

from database_utilities import db_utilities_bp

# app = Flask(__name__)
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

@app.before_request
def load_session_data():
    g.environment = session.get("environment")
    # print(g.environment)
    g.interface = session.get("interface")
    g.data = session.get("data", {})
    # print(g.data)


@app.route('/task-framework', strict_slashes=False, methods=["POST", "GET"])
def task_framework():
    return render_template('task_framework.html')



@app.route('/choose_env_interface', strict_slashes=False, methods=["POST", "GET"])
def env_interface():
    """ Endpoint to handle environment and interface selection """
    if request.method == "POST":
        try:
            passed_inputs = request.get_json()
            
            environment = passed_inputs.get('environment') if passed_inputs else None
            interface = passed_inputs.get('interface') if passed_inputs else None
            
            # global last_environment, last_interface, data
            
            # print(environment, session.get("environment"))
            if environment != session.get("environment"):
                g.data.clear()
                # ENVS_PATH = "envs"
                # DATA_PATH = f"{ENVS_PATH}/{environment}/data"
                # data_files = os.listdir(DATA_PATH)
                # # print("Loaded data:")
                # for data_file in data_files:
                #     if data_file.endswith(".json"):
                #         data_file_path = os.path.join(DATA_PATH, data_file)
                #         with open(data_file_path, "r") as file:
                #             g.data[data_file.split('.')[0]] = json.load(file)
                session["environment"] = environment
                session["interface"] = interface
                # session["data"] = g.data
                # print("data", g.data)
            
            # print(session["environment"], session["interface"])
            if environment and interface:
                # last_interface = interface
                # last_environment = environment
                ENVS_PATH = "envs"
                TOOLS_PATH = f"{ENVS_PATH}/{environment}/tools"
                INTERFACE_PATH = f"{TOOLS_PATH}/interface_{interface}"
                API_files = os.listdir(INTERFACE_PATH)
                invoke_methods = []
                functionsInfo = []
                importsSet = set()
                for api_file in API_files:
                    if api_file.endswith(".py") and not api_file.startswith("__"):
                        file_path = os.path.join(INTERFACE_PATH, api_file)
                        try:
                            function_info, invoke_method, imports = extract_file_info(file_path)
                            # print(f"Extracted function info: {function_info}")
                            # if not function_info:
                            #     print(f"No function info found in {api_file}, skipping.")
                            #     continue
                            importsSet.update(imports)
                            invoke_method = invoke_method.replace("invoke", function_info.get('name', 'invoke')+"_invoke")
                            invoke_methods.append(invoke_method)
                            functionsInfo.append(function_info)

                        except SyntaxError as e:
                            print(f"Syntax error in {api_file}: {e}")
                        except Exception as e:
                            print(f"Error processing {api_file}: {e}")
                
                # temp_dir = "/tmp"
                # tools_file_path = os.path.join(temp_dir, "tools.py")
                # with open(tools_file_path, "w") as new_file:
                #     new_file.write('\n'.join(sorted(importsSet)) + "\n\n")
                #     new_file.write("class Tools:\n")
                #     for invoke_method in invoke_methods:
                #         new_file.write("    @staticmethod\n" + invoke_method + "\n\n")
                session["imports_set"] = (importsSet)
                session["invoke_methods"] = invoke_methods
                session["actions"] = []
                # print("Imports set:", session["imports_set"])
                return jsonify({
                    'status': 'success',
                    'message': 'Environment and interface selected successfully',
                    'functions_info': functionsInfo,
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Missing environment or interface data'
                }), 400
                
        except Exception as e:
            print(f"Error processing request: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'{str(e)}'
            }), 500
    
    # Handle GET requests
    elif request.method == "GET":
        return jsonify({
            'status': 'success',
            'message': 'Choose environment and interface endpoint is working'
        })

def execute_api_utility(api_name, arguments):
    tools_instance = create_tools_class(session.get("imports_set", []), session.get("invoke_methods", []))
    # print('executing ...')
    arguments = arguments_processing(arguments)
    if hasattr(tools_instance, api_name):
        # try:
            # print(g.data)
            # Dynamically call the method with the provided arguments
            result = getattr(tools_instance, api_name)(data=g.data, **arguments)
            # print(f"Result from API {api_name}: {result}")
            # session["actions"].append({
            #     'api_name': api_name,
            #     'arguments': arguments
            # })
    #         return jsonify({
    #             'output': json.loads(result) if isinstance(result, str) else result
    #         }), 200
    #     except Exception as e:
    #         print(f"Error executing API {api_name}: {str(e)}")
    #         return jsonify({
    #             'status': 'error',
    #             'message': f'Failed to execute API: {str(e)}'
    #         }), 500
    # else:
    #     return jsonify({
    #         'status': 'error',
    #         'message': f'API {api_name} not found'
    #     }), 404


@app.route('/execute_api', strict_slashes=False, methods=["GET", "POST"])
def execute_api():
    # global data, last_environment, last_interface  # Add global declaration
    if request.method != "POST":
        return jsonify({
            'status': 'error',
            'message': 'Only POST requests are allowed'
        }), 405

    passed_data = request.get_json()
    # print(passed_data.get('environment'))
    environment = passed_data.get('environment', session.get("environment"))
    ENVS_PATH = "envs"
    DATA_PATH = f"{ENVS_PATH}/{environment}/data"
    data_files = os.listdir(DATA_PATH)
    # print("Loaded data:")
    for data_file in data_files:
        if data_file.endswith(".json"):
            data_file_path = os.path.join(DATA_PATH, data_file)
            with open(data_file_path, "r") as file:
                g.data[data_file.split('.')[0]] = json.load(file)
    
    for action in session.get("actions", []):
        # print('session:', session.get("actions"))
        api_name = action.get('api_name')
        execute_api_utility(api_name, action.get('arguments', {}))
    
    api_name = passed_data.get('api_name')
    api_name = api_name + "_invoke" if api_name else None
    if not api_name:
        return jsonify({
            'status': 'error',
            'message': 'API name is required'
        }), 400

    
    arguments = passed_data.get('parameters', {})
    cleaned_arguments = arguments_processing(arguments)
    arguments = cleaned_arguments
    
    
    tools_instance = create_tools_class(session.get("imports_set", []), session.get("invoke_methods", []))

    if hasattr(tools_instance, api_name):
        try:
            # print(g.data)
            # Dynamically call the method with the provided arguments
            result = getattr(tools_instance, api_name)(data=g.data, **arguments)
            # print(f"Result from API {api_name}: {result}")
            session["actions"].append({
                'api_name': api_name,
                'arguments': arguments
            })
            return jsonify({
                'output': json.loads(result) if isinstance(result, str) else result
            }), 200
        except Exception as e:
            print(f"Error executing API {api_name}: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to execute API: {str(e)}'
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': f'API {api_name} not found'
        }), 404

############# TASK TRACKER LOGIC ####################
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import threading
import base64

# Your Google Sheets functions
def connect_to_sheets():
    """Connect to Google Sheets with credentials"""
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    encoded = os.environ.get("CREDENTIAL_JSON_BASE64")

    if not encoded:
        raise ValueError("Missing credential JSON environment variable.")

    # Decode base64 to JSON string
    json_str = base64.b64decode(encoded).decode("utf-8")

    # Load JSON into dictionary
    credentials = json.loads(json_str)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    client = gspread.authorize(creds)
    return client

def get_sheet_data(sheet_name, worksheet_name):
    """Get all data from a specific worksheet"""
    client = connect_to_sheets()
    sheet = client.open(sheet_name).worksheet(worksheet_name)
    return sheet.get_all_values()

def print_sheet_data(all_rows, sheet_name):
    """Print all rows from sheet"""
    print(f"All rows from {sheet_name}:")
    for i, row in enumerate(all_rows):
        print(f"Row {i+1}: {row}")

# Example usage with different timeout methods
def run_with_timeout(func, args=(), kwargs=None, timeout_seconds=10):
    """
    Run a function with a timeout using threading
    """
    if kwargs is None:
        kwargs = {}
    
    result = [None]
    exception = [None]
    
    def target():
        try:
            result[0] = func(*args, **kwargs)
        except Exception as e:
            exception[0] = e
    
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()
    thread.join(timeout_seconds)
    
    if thread.is_alive():
        print(f"Function timed out after {timeout_seconds} seconds")
        return None
    
    if exception[0]:
        raise exception[0]
    
    return result[0]

###########################################################

@app.route('/tracker', strict_slashes=False, methods=["GET", "POST"])
def tracker():
    """ Endpoint to render the tracker page """
    if request.method == "POST":
        # Define the scope and credentials
        tasks_info = run_with_timeout(
        get_sheet_data, 
        args=('Amazon Agentic - Automated Tracking', 'Automated Tracker'),
        timeout_seconds=15
        )
        
        tasks_headers = tasks_info[0]
        tasks_rows = tasks_info[1:]

        list_of_tasks = []

        for row in tasks_rows:
            row_dict = dict(zip(tasks_headers, row))
            list_of_tasks.append(row_dict)

        
        username_email_mapping = run_with_timeout(
        get_sheet_data, 
        args=('Amazon Agentic - Automated Tracking', 'Username-email mapping'),
        timeout_seconds=15
        )
        
        username_email_mapping_headers = username_email_mapping[0]
        username_email_mapping_rows = username_email_mapping[1:]

        list_of_usernames = []

        for row in username_email_mapping_rows:
            row_dict = dict(zip(username_email_mapping_headers, row))
            list_of_usernames.append(row_dict)

        team_structure = run_with_timeout(
        get_sheet_data, 
        args=('Amazon Agentic - Automated Tracking', 'Team Structure'),
        timeout_seconds=15
        )
        
        team_headers = team_structure[0]
        team_rows = team_structure[1:]

        list_of_teams = []

        for row in team_rows:
            row_dict = dict(zip(team_headers, row))
            list_of_teams.append(row_dict)

        # if tasks_info:
        #     print_sheet_data(tasks_info, 'Automated Tracker')
        # else:
        #     print("Failed to fetch Automated Tracker data")
        
        # print("\n" + "="*50 + "\n")
        
        return jsonify({
            'status': 'success',
            'tasks_info': list_of_tasks,
            'username_email_mapping': list_of_usernames,
            'team_structure': list_of_teams
        }), 200
        
    return render_template('task_tracker.html')

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
