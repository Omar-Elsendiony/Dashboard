import os
from flask import Blueprint, render_template, request, jsonify
from modules.claude_apis import *

instruction_validation_bp = Blueprint('instruction_validation', __name__)


@instruction_validation_bp.route('/instruction_validation', strict_slashes=False, methods=["GET", "POST"])
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

@instruction_validation_bp.route('/instruction_relevant_actions_or_policies', strict_slashes=False, methods=["GET", "POST"])
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
@instruction_validation_bp.route('/google0798b17d9d33abf1.html')  # Replace with your actual filename
def google_verification():
    return 'google-site-verification: google0798b17d9d33abf1.html'  # Replace with actual content
