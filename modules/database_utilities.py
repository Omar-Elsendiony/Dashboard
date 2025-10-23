from flask import Blueprint, render_template
import os
from flask import request, jsonify
from dotenv import load_dotenv
load_dotenv()
# from openai import OpenAI
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

db_utilities_bp = Blueprint('db_utilities', __name__)


############ DB UTILITIES APIs ##############
@db_utilities_bp.route('/db_utilities', strict_slashes=False, methods=["GET", "POST"])
def db_utilities():
    """ Endpoint to render the DB connections page """
    if request.method == "POST":
        # Handle POST requests here if needed
        return jsonify({
            'status': 'success',
            'message': 'DB connections endpoint is working'
        }), 200
    
    # Handle GET requests
    return render_template('db_utilities.html')

@db_utilities_bp.route('/database_utilities_prompt_generation', methods=["POST"])
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
        # client = OpenAI() 
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
    elif action == "extract_policy_apis":
        initial_prompt = data.get('initial_prompt', '')
        policy = data.get('policy', '')
        example_apis = data.get('example_apis', '')
        
        prompt = initial_prompt.format(actions=example_apis, policy=policy)
        
        return jsonify({
            'status': 'success',
            'prompt': prompt
        }), 200
    elif action == "extract_policy_schema":
        example_schema = data.get('example_schema', '')
        policy = data.get('policy', '')
        initial_prompt = data.get('initial_prompt', '')

        prompt = initial_prompt.format(example_schema=example_schema, policy=policy)

        return jsonify({
            'status': 'success',
            'prompt': prompt
        }), 200
    elif action == "tune_policy":
        initial_prompt = data.get('initial_prompt', '')
        policy = data.get('policy', '')
        example_policies = data.get('example_policies', '')
        
        prompt = initial_prompt.format(
            policy=policy,
            example_policies=example_policies
        )
        
        return jsonify({
            'status': 'success',
            'prompt': prompt
        }), 200
    elif action == "validate_policy":
        initial_prompt = data.get('initial_prompt', '')
        policy = data.get('policy', '')
        example_policies = data.get('example_policies', '')
        
        prompt = initial_prompt.format(
            policy=policy,
            example_policies=example_policies
        )
        
        return jsonify({
            'status': 'success',
            'prompt': prompt
        }), 200
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid action'
        }), 400
    

@db_utilities_bp.route('/database_utilities', methods=["POST"])
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
    elif action == "extract_policy_apis":
        initial_prompt_file_path = f"prompts/extract_actions_from_policy/initial_prompt.txt"
        if not os.path.exists(initial_prompt_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Initial prompt file for {action} not found'
            }), 404

        with open(initial_prompt_file_path, 'r') as file:
            initial_prompt = file.read()

        example_apis_file_path = f"prompts/extract_actions_from_policy/examples_policy_actions.txt"
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
    elif action == "extract_policy_schema":
        initial_prompt_file_path = f"prompts/extract_schema_from_policy/initial_prompt.txt"
        if not os.path.exists(initial_prompt_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Initial prompt file for {action} not found'
            }), 404

        with open(initial_prompt_file_path, 'r') as file:
            initial_prompt = file.read()

        example_schema_file_path = f"prompts/extract_schema_from_policy/examples_schema.txt"
        if not os.path.exists(example_schema_file_path):
            return jsonify({
                'status': 'error',
                'message': f'Example schema file for {action} not found'
            }), 404

        with open(example_schema_file_path, 'r') as file:
            example_schema = file.read()

        return jsonify({
            'status': 'success',
            'initial_prompt': initial_prompt,
            'example_schema': example_schema
        }), 200
    elif action == 'tune_policy':
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

    elif action == 'policy_validator':
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
    else:
        return jsonify({
            'status': 'error',
            'message': 'Invalid action'
        }), 400
