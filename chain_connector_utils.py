# from typing import Tuple, List, Dict
# import os


# ################# CHAIN CONNECTOR ###############
# from chain_connector_utils import FunctionAnalyzer
# # Initialize the analyzer
# analyzer = FunctionAnalyzer()

# @app.route('/chain_analyzer', methods=['GET'])
# def chain_analyzer():
#     return render_template('chain_analyzer.html')

# @app.route('/api/load_python', methods=['POST'])
# def load_python():
#     data = request.get_json()
#     directory_path = data.get('directory_path', '')
    
#     if not directory_path:
#         return jsonify({'success': False, 'error': 'Directory path is required'})
    
#     try:
#         python_files, functions = analyzer.load_python_files_from_directory(directory_path)
        
#         # Store in session
#         session['python_files'] = python_files
#         session['functions'] = functions
        
#         return jsonify({
#             'success': True,
#             'python_files_count': len(python_files),
#             'functions_count': len(functions),
#             'functions': functions
#         })
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# @app.route('/api/load_json', methods=['POST'])
# def load_json():
#     data = request.get_json()
#     directory_path = data.get('directory_path', '')
    
#     if not directory_path:
#         return jsonify({'success': False, 'error': 'Directory path is required'})
    
#     try:
#         json_files = analyzer.load_json_files_from_directory(directory_path)
        
#         # Store in session
#         session['json_files'] = json_files
        
#         return jsonify({
#             'success': True,
#             'json_files_count': len(json_files),
#             'json_files': {name: {'structure': data['structure']} for name, data in json_files.items()}
#         })
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# @app.route('/api/get_json_data', methods=['POST'])
# def get_json_data():
#     data = request.get_json()
#     filename = data.get('filename', '')
    
#     json_files = session.get('json_files', {})
#     if filename not in json_files:
#         return jsonify({'success': False, 'error': 'File not found'})
    
#     return jsonify({
#         'success': True,
#         'data': json_files[filename]['data']
#     })

# @app.route('/api/analyze_chains', methods=['POST'])
# def analyze_chains():
#     data = request.get_json()
#     starting_variable = data.get('starting_variable', '')
    
#     if not starting_variable:
#         return jsonify({'success': False, 'error': 'Starting variable is required'})
    
#     functions = session.get('functions', {})
#     json_files = session.get('json_files', {})
    
#     if not functions:
#         return jsonify({'success': False, 'error': 'No functions loaded'})
    
#     try:
#         # Get debug info
#         matching_functions = []
#         for func_name, func_info in functions.items():
#             if analyzer._can_function_accept_input(func_info, starting_variable):
#                 matching_functions.append(func_name)
        
#         # Generate chains
#         chains = analyzer.suggest_chains(functions, {}, "", starting_variable)
        
#         return jsonify({
#             'success': True,
#             'functions_count': len(functions),
#             'matching_functions': matching_functions[:10],
#             'chains_count': len(chains),
#             'chains': chains
#         })
#     except Exception as e:
#         return jsonify({'success': False, 'error': str(e)})

# @app.route('/api/get_session_info', methods=['GET'])
# def get_session_info():
#     return jsonify({
#         'functions_count': len(session.get('functions', {})),
#         'json_files_count': len(session.get('json_files', {})),
#         'functions': session.get('functions', {}),
#         'json_files': {name: {'structure': data['structure']} for name, data in session.get('json_files', {}).items()}
#     })
# ########## END CHAIN CONNECTOR ##########


# class FunctionAnalyzer:
#     def __init__(self):
#         self.functions = {}
#         self.function_signatures = {}
#         self.json_files = {}
#         self.python_files = {}
    
#     def load_python_files_from_directory(self, directory_path: str) -> Tuple[Dict, Dict]:
#         """Load all Python files from a directory"""
#         python_files = {}
#         functions_found = {}
        
#         if not os.path.exists(directory_path):
#             return {}, {}
        
#         # Get all files except init files
#         all_files = glob.glob(os.path.join(directory_path, "*"))
#         py_files = [f for f in all_files if os.path.isfile(f) and 'init' not in os.path.basename(f).lower()]
        
#         for file_path in py_files:
#             file_name = os.path.basename(file_path)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = f.read()
#                     python_files[file_name] = content
                    
#                     # First try to parse classes and function definitions
#                     file_functions = self.parse_function_def(content)
                    
#                     # If no classes or functions found, treat the file itself as a function
#                     if not file_functions:
#                         # Extract parameters from the file content
#                         params = self._extract_params_from_content(content)
                        
#                         func_info = {
#                             'name': file_name,
#                             'args': params,
#                             'returns': None,
#                             'docstring': f"Function from file: {file_name}",
#                             'body': content[:200] + "..." if len(content) > 200 else content,
#                             'type': 'file_function',
#                             'outputs': ['result', 'data']
#                         }
#                         file_functions[file_name] = func_info
                    
#                     # Add all functions to the main collection
#                     for func_name, func_info in file_functions.items():
#                         func_info['source_file'] = file_name
#                         functions_found[func_name] = func_info
#             except:
#                 # Even if file reading fails, create a basic function entry
#                 func_info = {
#                     'name': file_name,
#                     'args': ['data'],  # Default parameter
#                     'returns': None,
#                     'docstring': f"Function from file: {file_name}",
#                     'body': "Could not read file content",
#                     'source_file': file_name,
#                     'type': 'file_function',
#                     'outputs': ['result', 'data']
#                 }
#                 functions_found[file_name] = func_info
                
#         return python_files, functions_found
    
#     def _extract_params_from_content(self, content: str) -> List[str]:
#         """Extract likely parameters from file content"""
#         params = []
        
#         # Look for common parameter patterns in the content
#         import re
        
#         # Look for variable assignments that might be parameters
#         param_patterns = [
#             r'(\w+_id)\s*=',
#             r'(\w+_data)\s*=',
#             r'(\w+_info)\s*=',
#             r'input\s*=\s*(\w+)',
#             r'data\s*=\s*(\w+)',
#             r'(\w+)\s*=\s*request',
#             r'(\w+)\s*=\s*input',
#         ]
        
#         for pattern in param_patterns:
#             matches = re.findall(pattern, content, re.IGNORECASE)
#             params.extend(matches)
        
#         # If no specific parameters found, add generic ones
#         if not params:
#             params = ['data', 'input', 'params']
        
#         # Remove duplicates and return
#         return list(set(params[:5]))  # Limit to 5 parameters
    
#     def load_json_files_from_directory(self, directory_path: str) -> Dict:
#         """Load all JSON files from a directory"""
#         json_files = {}
        
#         if not os.path.exists(directory_path):
#             return {}
        
#         json_file_paths = glob.glob(os.path.join(directory_path, "*.json"))
        
#         for file_path in json_file_paths:
#             file_name = os.path.basename(file_path)
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     content = json.load(f)
#                     json_files[file_name] = {
#                         'data': content,
#                         'structure': self._analyze_data_structure(content),
#                         'raw_content': json.dumps(content, indent=2)
#                     }
#             except:
#                 continue
                
#         return json_files
    
#     def parse_function_def(self, code_string: str) -> Dict:
#         """Parse Python classes and extract their invoke methods with proper inputs/outputs"""
#         try:
#             tree = ast.parse(code_string)
#             functions = {}
            
#             # Look for classes with invoke methods
#             for node in ast.walk(tree):
#                 if isinstance(node, ast.ClassDef):
#                     class_name = node.name
                    
#                     # Look for invoke method in this class
#                     invoke_method = None
#                     for class_item in node.body:
#                         if (isinstance(class_item, ast.FunctionDef) and 
#                             class_item.name == 'invoke'):
#                             invoke_method = class_item
#                             break
                    
#                     if invoke_method:
#                         # Extract actual parameters (excluding 'self')
#                         params = [arg.arg for arg in invoke_method.args.args if arg.arg != 'self']
                        
#                         # Extract outputs by analyzing the invoke method body
#                         outputs = self._extract_outputs_from_invoke_method(invoke_method, class_name)
                        
#                         func_info = {
#                             'name': class_name,
#                             'args': params,
#                             'returns': self._get_return_annotation(invoke_method),
#                             'docstring': ast.get_docstring(invoke_method) or ast.get_docstring(node),
#                             'body': ast.unparse(invoke_method) if hasattr(ast, 'unparse') else str(invoke_method),
#                             'type': 'class_invoke',
#                             'class_name': class_name,
#                             'outputs': outputs,
#                             'raw_code': code_string[:500]  # Store raw code for debugging
#                         }
#                         functions[class_name] = func_info
#                     else:
#                         # Class without invoke method - create basic entry
#                         func_info = {
#                             'name': class_name,
#                             'args': ['input_data'],  # Default parameter
#                             'returns': None,
#                             'docstring': ast.get_docstring(node) or f"Class: {class_name}",
#                             'body': f"class {class_name}",
#                             'type': 'class_no_invoke',
#                             'class_name': class_name,
#                             'outputs': ['result'],
#                             'raw_code': code_string[:500]
#                         }
#                         functions[class_name] = func_info
                    
#             return functions
#         except Exception as e:
#             # If parsing fails, try to extract class name from the code manually
#             return self._fallback_class_extraction(code_string, str(e))
    
#     def _extract_outputs_from_invoke_method(self, invoke_method, class_name: str) -> List[str]:
#         """Extract outputs by analyzing the invoke method body more thoroughly"""
#         outputs = []
        
#         # Look for return statements
#         for node in ast.walk(invoke_method):
#             if isinstance(node, ast.Return) and node.value:
#                 outputs.extend(self._parse_return_value(node.value))
        
#         # Look for variable assignments that might be outputs
#         for node in ast.walk(invoke_method):
#             if isinstance(node, ast.Assign):
#                 for target in node.targets:
#                     if isinstance(target, ast.Name):
#                         var_name = target.id
#                         # Common output variable patterns
#                         if any(pattern in var_name.lower() for pattern in 
#                                ['result', 'output', 'response', 'data', 'info']):
#                             outputs.append(var_name)
        
#         # Extract from class name patterns
#         name_outputs = self._extract_outputs_from_name(class_name)
#         outputs.extend(name_outputs)
        
#         # Remove duplicates and return
#         return list(set(outputs)) if outputs else ['result']
    
#     def _parse_return_value(self, return_node) -> List[str]:
#         """Parse different types of return values"""
#         outputs = []
        
#         if isinstance(return_node, ast.Dict):
#             # return {"key1": value1, "key2": value2}
#             for key in return_node.keys:
#                 if isinstance(key, ast.Constant):
#                     outputs.append(str(key.value))
#                 elif hasattr(key, 's'):  # Python < 3.8
#                     outputs.append(key.s)
        
#         elif isinstance(return_node, ast.Name):
#             # return variable_name
#             outputs.append(return_node.id)
        
#         elif isinstance(return_node, ast.Tuple) or isinstance(return_node, ast.List):
#             # return (a, b, c) or return [a, b, c]
#             for elt in return_node.elts:
#                 if isinstance(elt, ast.Name):
#                     outputs.append(elt.id)
#                 elif isinstance(elt, ast.Constant):
#                     outputs.append(str(elt.value))
        
#         elif isinstance(return_node, ast.Call):
#             # return function_call()
#             if isinstance(return_node.func, ast.Name):
#                 func_name = return_node.func.id
#                 outputs.append(f"{func_name}_result")
        
#         return outputs
    
#     def _fallback_class_extraction(self, code_string: str, error: str) -> Dict:
#         """Fallback method to extract class info when AST parsing fails"""
#         functions = {}
        
#         # Use regex to find class definitions
#         import re
#         class_pattern = r'class\s+(\w+)(?:\([^)]*\))?:'
#         matches = re.findall(class_pattern, code_string)
        
#         for class_name in matches:
#             func_info = {
#                 'name': class_name,
#                 'args': ['input_data'],
#                 'returns': None,
#                 'docstring': f"Class: {class_name} (fallback parsing)",
#                 'body': f"class {class_name}",
#                 'type': 'class_fallback',
#                 'class_name': class_name,
#                 'outputs': ['result'],
#                 'parse_error': error,
#                 'raw_code': code_string[:500]
#             }
#             functions[class_name] = func_info
        
#         return functions
    
#     def _extract_outputs_from_name(self, name: str) -> List[str]:
#         """Extract likely outputs from function/class name"""
#         outputs = []
#         name_lower = name.lower()
        
#         # Extract entities from function names
#         common_entities = ['user', 'incident', 'task', 'comment', 'attachment', 'department', 
#                           'category', 'company', 'article', 'change', 'request', 'overdue']
        
#         for entity in common_entities:
#             if entity in name_lower:
#                 outputs.append(entity)
#                 outputs.append(entity + '_data')
#                 outputs.append(entity + '_info')
        
#         # Based on function action patterns
#         if any(action in name_lower for action in ['get', 'fetch', 'retrieve']):
#             outputs.extend(['data', 'result', 'info', 'details'])
        
#         if any(action in name_lower for action in ['create', 'add', 'insert']):
#             outputs.extend(['created_item', 'new_item', 'id'])
        
#         if any(action in name_lower for action in ['filter', 'search', 'find']):
#             outputs.extend(['filtered_data', 'results', 'list'])
        
#         if any(action in name_lower for action in ['update', 'modify', 'edit']):
#             outputs.extend(['updated_item', 'status'])
        
#         return outputs
    
#     def _get_return_annotation(self, node):
#         """Extract return type annotation if present"""
#         if node.returns:
#             if hasattr(ast, 'unparse'):
#                 return ast.unparse(node.returns)
#             else:
#                 return str(node.returns)
#         return None
    
#     def _analyze_data_structure(self, data, path="root"):
#         """Recursively analyze data structure"""
#         structure = {"type": type(data).__name__, "path": path}
        
#         if isinstance(data, dict):
#             structure["keys"] = list(data.keys())
#             structure["nested"] = {}
#             for key, value in data.items():
#                 structure["nested"][key] = self._analyze_data_structure(value, f"{path}.{key}")
#         elif isinstance(data, list) and data:
#             structure["length"] = len(data)
#             structure["item_type"] = type(data[0]).__name__
#             if isinstance(data[0], (dict, list)):
#                 structure["item_structure"] = self._analyze_data_structure(data[0], f"{path}[0]")
        
#         return structure
    
#     def suggest_chains(self, functions: Dict, json_structure: Dict, initial_instruction: str, starting_variable: str = None) -> List[Dict]:
#         """Build chains by following input->output->input flow"""
#         if not starting_variable:
#             return []
        
#         chains = []
        
#         # Find functions that can accept the starting variable
#         starter_functions = self._find_functions_that_accept(starting_variable, functions)
        
#         # Build multiple chains starting from different functions
#         for starter_func in starter_functions[:5]:  # Try top 5 starters
#             chain = self._build_single_chain(starting_variable, starter_func, functions, max_length=40)
#             if len(chain['steps']) >= 3:  # Only keep chains with at least 3 steps
#                 chains.append(chain)
        
#         return chains[:3]  # Return top 3 chains
    
#     def _find_functions_that_accept(self, input_var: str, functions: Dict) -> List[str]:
#         """Find functions that can actually accept the input variable"""
#         matching_functions = []
        
#         for func_name, func_info in functions.items():
#             if self._can_function_accept_input(func_info, input_var):
#                 matching_functions.append(func_name)
        
#         return matching_functions
    
#     def _can_function_accept_input(self, func_info: Dict, potential_input: str) -> bool:
#         """Check if a function can accept a particular input based on parameter names"""
#         input_lower = potential_input.lower()
        
#         # Make sure input is not the same as any of the function's outputs
#         outputs = func_info.get('outputs', [])
#         for output in outputs:
#             if input_lower == output.lower():
#                 return False  # Input can't be same as output
        
#         # Only accept if there's a meaningful parameter match
#         for param in func_info['args']:
#             param_lower = param.lower()
            
#             # Exact or partial name matching
#             if input_lower == param_lower:  # Exact match
#                 return True
#             if input_lower in param_lower and len(input_lower) > 2:  # Partial match (avoid short matches)
#                 return True
#             if param_lower in input_lower and len(param_lower) > 2:
#                 return True
        
#         return False
    
#     def _build_single_chain(self, starting_var: str, start_func: str, functions: Dict, max_length: int = 40) -> Dict:
#         """Build a single chain following input->output->input flow"""
#         steps = []
#         current_var = starting_var
#         used_functions = set()
#         used_variables = {starting_var.lower()}  # Track used variables to avoid repetition
        
#         # Start with the initial function
#         current_func = start_func
        
#         for i in range(max_length):
#             if current_func in used_functions:
#                 break  # Avoid cycles
            
#             if current_func not in functions:
#                 break  # Function not found
            
#             used_functions.add(current_func)
#             func_info = functions.get(current_func, {})
            
#             # Get outputs from current function
#             outputs = self._extract_potential_outputs(current_func, func_info)
#             if not outputs:
#                 outputs = ['result']  # Default output
            
#             # Pick the first meaningful output that hasn't been used
#             chosen_output = self._pick_unused_output(outputs, used_variables, current_func)
#             if not chosen_output:
#                 break  # No unused outputs available
            
#             # Get all required inputs for this function
#             required_inputs = func_info.get('args', [])
#             other_inputs = [inp for inp in required_inputs if inp.lower() != current_var.lower()]
            
#             # Add this step to the chain
#             step = {
#                 'input': current_var,
#                 'function': current_func,
#                 'all_required_inputs': required_inputs,
#                 'other_inputs_needed': other_inputs,
#                 'outputs': outputs,
#                 'chosen_output': chosen_output
#             }
#             steps.append(step)
            
#             # Mark this output as used
#             used_variables.add(chosen_output.lower())
            
#             # Find next function that can accept this output
#             next_functions = self._find_functions_that_accept(chosen_output, functions)
#             next_functions = [f for f in next_functions if f not in used_functions]  # Exclude used
            
#             if not next_functions:
#                 # Try with alternative unused outputs if no function found
#                 for alt_output in outputs[1:]:
#                     if alt_output.lower() not in used_variables:  # Only try unused outputs
#                         alt_next_functions = self._find_functions_that_accept(alt_output, functions)
#                         alt_next_functions = [f for f in alt_next_functions if f not in used_functions]
#                         if alt_next_functions:
#                             chosen_output = alt_output
#                             steps[-1]['chosen_output'] = chosen_output  # Update the step
#                             used_variables.add(chosen_output.lower())  # Mark as used
#                             next_functions = alt_next_functions
#                             break
                
#                 if not next_functions:
#                     break  # No more functions can accept any unused output
            
#             # Pick the next function (could be random, or based on some logic)
#             current_func = next_functions[0]  # Take first available
#             current_var = chosen_output  # This becomes the input for next function
        
#         # Build description
#         description_parts = [starting_var]
#         for step in steps:
#             description_parts.append(f"{step['function']}({step['chosen_output']})")
        
#         return {
#             'chain': [step['function'] for step in steps],
#             'steps': steps,
#             'description': ' → '.join(description_parts),
#             'starting_variable': starting_var,
#             'length': len(steps),
#             'confidence': min(1.0, len(steps) / 20.0),
#             'unique_variables': list(used_variables)
#         }
    
#     def _extract_potential_outputs(self, func_name: str, func_info: Dict) -> List[str]:
#         """Extract what this function outputs - use parsed outputs if available"""
#         # If we have parsed outputs from the AST, use those first
#         if 'outputs' in func_info and func_info['outputs']:
#             return func_info['outputs']
        
#         # Fallback to name-based extraction
#         return self._extract_outputs_from_name(func_name)
    
#     def _pick_unused_output(self, outputs: List[str], used_variables: set, func_name: str) -> str:
#         """Pick the most meaningful output that hasn't been used yet"""
#         if not outputs:
#             return None
        
#         # Filter out already used outputs
#         unused_outputs = [o for o in outputs if o.lower() not in used_variables]
#         if not unused_outputs:
#             return None  # All outputs have been used
        
#         # Prefer outputs that match the function name
#         func_lower = func_name.lower()
#         for output in unused_outputs:
#             if any(word in output.lower() for word in func_lower.split('_')):
#                 return output
        
#         # Prefer non-generic outputs
#         non_generic = [o for o in unused_outputs if o.lower() not in ['result', 'data', 'output', 'response']]
#         if non_generic:
#             return non_generic[0]
        
#         # Fall back to first unused output
#         return unused_outputs[0]


