#!/usr/bin/python3
""" Flask Application """
import json
import os
import redis
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import ast
from typing import Dict, Any
import re
from flask import Flask, session, g
from flask_session import Session
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
from datetime import timedelta
load_dotenv()


# app = Flask(__name__)
app = Flask(__name__ , static_url_path='')
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key")
cors = CORS(app)
app.config["SESSION_PERMANENT"] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10) 

# app.config['SESSION_TYPE'] = 'filesystem' 

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.from_url(os.environ.get('REDIS_URL'))
Session(app)

###################### GLOBAL ENVIRONMENTS ##################################
# last_environment = None
# last_interface = None
# data = dict()

@app.before_request
def load_session_data():
    g.environment = session.get("environment")
    # print(g.environment)
    g.interface = session.get("interface")
    g.data = session.get("data", {})
    # print(g.data)

######################## UTILITY FUNCTIONS ##################################
def ast_to_python_value(node):
    """Convert AST node to Python value."""
    if isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    elif isinstance(node, ast.Str):  # Python < 3.8
        return node.s
    elif isinstance(node, ast.Num):  # Python < 3.8
        return node.n
    elif isinstance(node, ast.List):
        return [ast_to_python_value(item) for item in node.elts]
    elif isinstance(node, ast.Dict):
        result = {}
        for key, value in zip(node.keys, node.values):
            result[ast_to_python_value(key)] = ast_to_python_value(value)
        return result
    elif isinstance(node, ast.Name):
        # For variable names, we can't resolve them without execution
        # Return the name as a string for now
        return f"<variable: {node.id}>"
    else:
        # For other node types, return a string representation
        return f"<{type(node).__name__}>"


def extract_method_from_ast(source_code: str, method_name: str) -> str:
    tree = ast.parse(source_code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == method_name:
            start = node.lineno - 1
            end = node.end_lineno
            return '\n'.join(source_code.splitlines()[start:end])
    return None


def extract_file_info(file_path: str) -> Dict[str, Any]:
    """
    Extract function information from a Python file containing a Tool class with get_info method.
    """
    try:
        # Read the file content
        with open(file_path, "r") as file:
            content = file.read()
        
        imports = []
        import_pattern = re.compile(r'^\s*import\s+(\w+)', re.MULTILINE)
        from_import_pattern =  re.compile(r'^\s*from\s+([\w\.]+)\s+import\s+((?:\w+\s*,\s*)*\w+)', re.MULTILINE)
        
        for match in import_pattern.finditer(content):
            imports.append(match.group(0).strip())
        for match in from_import_pattern.finditer(content):
            if match.group(1) == "tau_bench.envs.tool":
                # Skip tau_bench.envs.tool import
                continue
            imports.append(match.group(0).strip())
        
        tree = ast.parse(content)
        
        tool_class = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    if isinstance(base, ast.Name) and base.id == 'Tool':
                        tool_class = node
                        # break
            if isinstance(node, ast.FunctionDef) and node.name == "invoke":
                start = node.lineno - 1
                end = node.end_lineno
                invoke_method = '\n'.join(content.splitlines()[start:end])
                # if tool_class:
                #     break
        
        if not tool_class:
            return {"error": "No Tool class found"}
        
        if not invoke_method:
            return {"error": "No invoke method found in Tool class"}
        
        # Find the get_info method
        get_info_method = None
        for node in tool_class.body:
            if isinstance(node, ast.FunctionDef) and node.name == 'get_info':
                get_info_method = node
                break
        
        if not get_info_method:
            return {"error": "No get_info method found"}
        
        return_dict = None
        for node in ast.walk(get_info_method):
            if isinstance(node, ast.Return):
                return_dict = node.value
                break
        
        if not return_dict:
            return {"error": "No return dictionary found in get_info method"}
        
        parsed_dict = ast_to_python_value(return_dict)
        function_info = {}
        
        if isinstance(parsed_dict, dict) and 'function' in parsed_dict:
            func_info = parsed_dict['function']
            if isinstance(func_info, dict):
                function_info = {
                    'name': func_info.get('name', ''),
                    'description': func_info.get('description', ''),
                    'parameters': func_info.get('parameters', {}).get('properties', {}),
                    'required': func_info.get('parameters', {}).get('required', [])
                }

        return function_info, invoke_method, imports
        
    except Exception as e:
        return {"error": f"Failed to process file: {str(e)}"}
######################## END UTILITY FUNCTIONS ##############################


@app.route('/task-framework', strict_slashes=False, methods=["POST", "GET"])
def task_framework():
    return render_template('task_framework.html')

def create_tools_class(imports_set, invoke_methods):
    # Create the class dynamically in memory
    imports_code = '\n'.join(sorted(imports_set))
    
    # Build the class definition as a string
    class_code = f"""
{imports_code}

class Tools:
"""
    for invoke_method in invoke_methods:
        class_code += ("    @staticmethod\n" + invoke_method + "\n\n")
    # Execute the code and return the class
    namespace = {}
    exec(class_code, namespace)
    # return namespace['Tools']
    # session["tools_class_code"] = class_code 
    return namespace['Tools']


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
    print('executing ...')
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

def arguments_processing(arguments):
    cleaned_arguments = {}
    for argument, argument_value in arguments.items():
        # Skip empty values
        if argument_value == '':
            continue

        # Skip IDs (do not modify or parse)
        if "id" == argument.lower() or "_id" in argument.lower() or "_by" in argument.lower() or "name" in argument.lower() or "_to" in argument.lower():
            cleaned_arguments[argument] = argument_value
            continue
        # Try to evaluate literal (e.g., convert "True" → True, "123" → 123)
        try:
            cleaned_arguments[argument] = ast.literal_eval(argument_value)
        except (ValueError, SyntaxError):
            cleaned_arguments[argument] = argument_value

    return cleaned_arguments

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
        print('session:', session.get("actions"))
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
            print(f"Result from API {api_name}: {result}")
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

################# CHAIN CONNECTOR ###############
from utils import FunctionAnalyzer
# Initialize the analyzer
analyzer = FunctionAnalyzer()

@app.route('/chain_analyzer', methods=['GET'])
def chain_analyzer():
    return render_template('chain_analyzer.html')

@app.route('/api/load_python', methods=['POST'])
def load_python():
    data = request.get_json()
    directory_path = data.get('directory_path', '')
    
    if not directory_path:
        return jsonify({'success': False, 'error': 'Directory path is required'})
    
    try:
        python_files, functions = analyzer.load_python_files_from_directory(directory_path)
        
        # Store in session
        session['python_files'] = python_files
        session['functions'] = functions
        
        return jsonify({
            'success': True,
            'python_files_count': len(python_files),
            'functions_count': len(functions),
            'functions': functions
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/load_json', methods=['POST'])
def load_json():
    data = request.get_json()
    directory_path = data.get('directory_path', '')
    
    if not directory_path:
        return jsonify({'success': False, 'error': 'Directory path is required'})
    
    try:
        json_files = analyzer.load_json_files_from_directory(directory_path)
        
        # Store in session
        session['json_files'] = json_files
        
        return jsonify({
            'success': True,
            'json_files_count': len(json_files),
            'json_files': {name: {'structure': data['structure']} for name, data in json_files.items()}
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_json_data', methods=['POST'])
def get_json_data():
    data = request.get_json()
    filename = data.get('filename', '')
    
    json_files = session.get('json_files', {})
    if filename not in json_files:
        return jsonify({'success': False, 'error': 'File not found'})
    
    return jsonify({
        'success': True,
        'data': json_files[filename]['data']
    })

@app.route('/api/analyze_chains', methods=['POST'])
def analyze_chains():
    data = request.get_json()
    starting_variable = data.get('starting_variable', '')
    
    if not starting_variable:
        return jsonify({'success': False, 'error': 'Starting variable is required'})
    
    functions = session.get('functions', {})
    json_files = session.get('json_files', {})
    
    if not functions:
        return jsonify({'success': False, 'error': 'No functions loaded'})
    
    try:
        # Get debug info
        matching_functions = []
        for func_name, func_info in functions.items():
            if analyzer._can_function_accept_input(func_info, starting_variable):
                matching_functions.append(func_name)
        
        # Generate chains
        chains = analyzer.suggest_chains(functions, {}, "", starting_variable)
        
        return jsonify({
            'success': True,
            'functions_count': len(functions),
            'matching_functions': matching_functions[:10],
            'chains_count': len(chains),
            'chains': chains
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/get_session_info', methods=['GET'])
def get_session_info():
    return jsonify({
        'functions_count': len(session.get('functions', {})),
        'json_files_count': len(session.get('json_files', {})),
        'functions': session.get('functions', {}),
        'json_files': {name: {'structure': data['structure']} for name, data in session.get('json_files', {}).items()}
    })
########## END CHAIN CONNECTOR ##########

############ DB UTILITIES APIs ##############
@app.route('/db_connections', strict_slashes=False, methods=["GET", "POST"])
def db_connections():
    """ Endpoint to render the DB connections page """
    if request.method == "POST":
        # Handle POST requests here if needed
        return jsonify({
            'status': 'success',
            'message': 'DB connections endpoint is working'
        }), 200
    
    # Handle GET requests
    return render_template('db_connections.html')

@app.route('/database_utilities_prompt_generation', methods=["POST"])
def database_utilities_prompt_generation():
    """ Endpoint to generate prompts for database utilities """
    data = request.get_json()
    
    action = data.get('action')
    if not action:
        return jsonify({
            'status': 'error',
            'message': 'Action is required'
        }), 400
    
    if action == "generate_policy_prompt":
        db_schema = data.get('db_schema', '')
        example_policies = data.get('example_policies', '')
        interface_apis = data.get('interface_apis', '')
        initial_prompt = data.get('initial_prompt', '')
        
        prompt = initial_prompt.format(
            db_schema=db_schema,
            example_policy_document=example_policies,
            apis_documentation=interface_apis
        )
        
        return jsonify({
            'status': 'success',
            'prompt': prompt
        }), 200
    elif action == "generate_api_prompt":
        db_schema = data.get('db_schema', '')
        example_apis = data.get('example_apis', '')
        initial_prompt = data.get('initial_prompt', '')
        interface_apis = data.get('interface_apis', '')
        
        prompt = initial_prompt.format(
            db_schema=db_schema,
            examples_tools=example_apis,
            required_tools=interface_apis
        )
        print(prompt)
        
        return jsonify({
            'status': 'success',
            'prompt': prompt
        }), 200
    elif action == "generate_seed_prompt":
        db_schema = data.get('db_schema', '')
        # example_data = data.get('example_data', '')
        initial_prompt = data.get('initial_prompt', '')
        
        prompt = initial_prompt.format(
            db_schema=db_schema,
            # example_data_document=example_data
        )
        
        return jsonify({
            'status': 'success',
            'prompt': prompt
        }), 200
    elif action == "generate_scenario_prompt":
        db_schema = data.get('db_schema', '')
        # example_scenarios = data.get('example_scenarios', '')
        initial_prompt = data.get('initial_prompt', '')
        
        prompt = initial_prompt.format(
            db_schema=db_schema,
            # example_scenarios=example_scenarios
        )
        
        return jsonify({
            'status': 'success',
            'prompt': prompt
        }), 200
    elif action == "check_scenario_realism":
        from openai import OpenAI

        client = OpenAI() 
        db_schema = data.get('db_schema', '')
        scenario = data.get('scenario', '')
        
        if not db_schema or not scenario:
            return jsonify({
                'status': 'error',
                'message': 'db_schema and scenario are required'
            }), 400
        
        prompt = f"Check the realism of the following scenario based on the provided database schema:\n\nDatabase Schema:\n{db_schema}\n\nScenario:\n{scenario}\n\nIs this scenario realistic? Please provide a detailed explanation."
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            realism_check = response.choices[0].message.content.strip()
            return jsonify({
                'status': 'success',
                'realism_check': realism_check
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Failed to check scenario realism: {str(e)}'
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid action'
        }), 400
    

@app.route('/database_utilities', methods=["POST"])
def database_utilities():
    data = request.get_json()
    
    action = data.get('action')
    if action == 'policy_creation':
        # Handle policy creation logic here
        initial_prompt_file_path = f"prompts/{action}/initial_prompt.txt"
        if not os.path.exists(initial_prompt_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Initial prompt file for {action} not found'
            }), 404
        
        with open(initial_prompt_file_path, 'r') as file:
            initial_prompt = file.read()
        
        example_policies_file_path = f"prompts/{action}/example_policies.txt"
        if not os.path.exists(example_policies_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Example policies file for {action} not found'
            }), 404
        
        with open(example_policies_file_path, 'r') as file:
            example_policies = file.read()
        
        
        return jsonify({
            'status': 'success',
            'initial_prompt': initial_prompt,
            'example_policies': example_policies
        }), 200
        
    elif action == 'api_implementation':
        # Handle API implementation logic here
        initial_prompt_file_path = f"prompts/{action}/initial_prompt.txt"
        if not os.path.exists(initial_prompt_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Initial prompt file for {action} not found'
            }), 404
        
        with open(initial_prompt_file_path, 'r') as file:
            initial_prompt = file.read()
        
        example_apis_file_path = f"prompts/{action}/examples_tools.txt" # aka example APIs
        if not os.path.exists(example_apis_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Example APIs file for {action} not found'
            }), 404
        
        with open(example_apis_file_path, 'r') as file:
            example_apis = file.read()
        
        return jsonify({
            'status': 'success',
            'initial_prompt': initial_prompt,
            'example_apis': example_apis
        }), 200
        
    elif action == 'database_seeding':
        # Handle database seeding logic here
        initial_prompt_file_path = f"prompts/{action}/initial_prompt.txt"
        if not os.path.exists(initial_prompt_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Initial prompt file for {action} not found'
            }), 404
        with open(initial_prompt_file_path, 'r') as file:
            initial_prompt = file.read()
        # example_data_file_path = f"prompts/{action}/example_data.txt"
        # if not os.path.exists(example_data_file_path):
        #     return jsonify({
        #         'status': 'error',
        #         'message': f'Example data file for {action} not found'
        #     }), 404
        # with open(example_data_file_path, 'r') as file:
        #     example_data = file.read()
        
        return jsonify({
            'status': 'success',
            'initial_prompt': initial_prompt
        }), 200
    elif action == 'scenario_realism':
        # Handle scenario realism logic here
        initial_prompt_file_path = f"prompts/{action}/initial_prompt.txt"
        if not os.path.exists(initial_prompt_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Initial prompt file for {action} not found'
            }), 404
        
        with open(initial_prompt_file_path, 'r') as file:
            initial_prompt = file.read()
        
        # example_scenarios_file_path = f"prompts/{action}/example_scenarios.txt"
        # if not os.path.exists(example_scenarios_file_path):
        #     return jsonify({
        #         'status': 'error',
        #         'message': f'Example scenarios file for {action} not found'
        #     }), 404
        
        # with open(example_scenarios_file_path, 'r') as file:
        #     example_scenarios = file.read()
        
        return jsonify({
            'status': 'success',
            'initial_prompt': initial_prompt,
            # 'example_scenarios': example_scenarios
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid action'
        }), 400

@app.route('/instruction_validation', strict_slashes=False, methods=["GET", "POST"])
def task_validation():
    if request.method == "POST":
        data = request.json
        # Process the task validation request
        return jsonify({
            'status': 'success',
            'message': 'Task validation initiated'
        }), 200
    return render_template('instruction_validation.html')

if __name__ == "__main__":
    """ Main Function """
    # host = '0.0.0.0'
    # port = 5000
    app.run()
