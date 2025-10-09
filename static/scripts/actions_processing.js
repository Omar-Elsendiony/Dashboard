
const APIs = new Map();
let actionCounter = 0;

async function handleGo() {
    const environment = document.getElementById('environment').value.trim();
    const interface = document.getElementById('interface').value;
    
    if (!environment) {
        showWrongMessage('Please enter an environment name');
        return;
    }
    
    if (!interface) {
        showWrongMessage('Please select an interface');
        return;
    }
    
    console.log('Environment:', environment);
    console.log('Interface:', interface);
    
    try {
        const response = await fetch('/choose_env_interface', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                environment: environment,
                interface: interface
            })
        });

        if (!response.ok) {
            showWrongMessage('Failed to select Environment and Interface.');
            console.error('Error details:', await response.json());
            return;
        }

        const data = await response.json();
        if (data.status === 'success') {
            showCorrectMessage('Environment and Interface selected successfully!');
            console.log('Response:', data);
            
            // Clear existing APIs
            APIs.clear();
            
            // Populate APIs from response
            for (const func of data.functions_info) {
                APIs.set(func.name, {
                    description: func.description,
                    parameters: func.parameters,
                    required: func.required
                });
            }
            console.log('APIs:', APIs);
        } else {
            showWrongMessage('Failed to select Environment and Interface.');
        }
    } catch (error) {
        console.error('Error:', error);
        showWrongMessage('An error occurred while connecting to the server.');
    
    }
}

async function runAllActions() {
    const actionElements = document.querySelectorAll('.api-action');
    const runAllBtn = document.getElementById('run-all-btn');
    
    if (actionElements.length === 0) {
        showWrongMessage('No actions to execute.');
        return;
    }
    
    // Check if all actions have selected APIs
    let hasInvalidActions = false;
    actionElements.forEach((actionEl, index) => {
        const selectedRadio = actionEl.querySelector('input[type="radio"]:checked');
        if (!selectedRadio) {
            showWrongMessage(`Action ${index + 1} doesn't have an API selected.`);
            hasInvalidActions = true;
        }
    });
    
    if (hasInvalidActions) {
        return;
    }
    
    // Disable the run all button
    runAllBtn.textContent = '⏳ Running All Actions...';
    runAllBtn.disabled = true;
    
    let successCount = 0;
    let errorCount = 0;
    
    try {
        for (let i = 0; i < actionElements.length; i++) {
            const actionEl = actionElements[i];
            const actionId = actionEl.id;
            
            showCorrectMessage(`Executing Action ${i + 1} of ${actionElements.length}...`);
            
            try {
                await executeAPI(actionId);
                successCount++;
            } catch (error) {
                console.error(`Error executing action ${i + 1}:`, error);
                errorCount++;
            }
            
            // Wait 1 seconds before next action (except for the last one)
            if (i < actionElements.length - 1) {
                await new Promise(resolve => setTimeout(resolve, 1000));
            }
        }
        
        // Show final summary
        if (errorCount === 0) {
            showCorrectMessage(`All ${successCount} actions executed successfully!`);
        } else {
            showWrongMessage(`Execution completed: ${successCount} successful, ${errorCount} failed.`);
        }
        
    } catch (error) {
        console.error('Error in runAllActions:', error);
        showWrongMessage('An error occurred while running actions.');
    } finally {
        // Re-enable the button
        runAllBtn.textContent = '🚀 Run All Actions';
        runAllBtn.disabled = false;
    }
}

function addAction() {
    if (APIs.size === 0) {
        showWrongMessage('Please select an environment and interface first by clicking GO.');
        return [ null, null ];
    }

    actionCounter++;
    const actionId = `action_${actionCounter}`;
    
    const actionContainer = document.getElementById('api-actions-container');
    
    const actionDiv = document.createElement('div');
    actionDiv.className = 'api-action';
    actionDiv.id = actionId;
    
    actionDiv.innerHTML = `
        <div class="api-action-header">
            <div class="api-action-title">Action</div>
            <button class="remove-action-button" onclick="removeAction('${actionId}')">×</button>
        </div>
                                        
        <div class="form-group">
            <label class="form-label">Select API</label>
            <div class="radio-button-container" id="${actionId}_radio_container">
                ${Array.from(APIs.keys()).map(apiKey => `
                    <input type="radio" 
                        id="${actionId}_${apiKey}" 
                        name="${actionId}_api" 
                        value="${apiKey}" 
                        class="radio-input"
                        onchange="selectAPI('${actionId}', this.value)">
                    <label for="${actionId}_${apiKey}" class="radio-button">${apiKey}</label>
                `).join('')}
            </div>
        </div>

        
        <div id="${actionId}_description" class="api-description" style="display: none;"></div>
        <div id="${actionId}_parameters" class="parameters-container"></div>
        <div id="${actionId}_execute" style="display: none;">
            <button class="execute-button" onclick="executeAPI('${actionId}')">
                🚀 Execute API
            </button>
        </div>
        <div id="${actionId}_response" class="api-response"></div>
    `;
    document.getElementsByClassName('add-action-container')[0].remove();
    const addAction = document.createElement('div');
    addAction.className = 'add-action-container';
    addAction.style = "height: 100px; display: flex; justify-content: center; align-items: center; flex-direction: column;"
    addAction.innerHTML = `
        <button class="add-action-button" onclick="addAction()">
            +
        </button>
        <span class="add-action-text">Add Action</span>
    `;
    
    actionContainer.appendChild(actionDiv);
    actionContainer.appendChild(addAction);
    
    // Scroll to the new action
    actionDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
    return [actionId, actionDiv];
}

function removeAction(actionId) {
    const actionDiv = document.getElementById(actionId);
    actionCounter--;
    if (actionDiv) {
        actionDiv.remove();
    }
}

function selectAPI(actionId, apiKey) {
    const descriptionDiv = document.getElementById(`${actionId}_description`);
    const parametersDiv = document.getElementById(`${actionId}_parameters`);
    const executeDiv = document.getElementById(`${actionId}_execute`);
    const responseDiv = document.getElementById(`${actionId}_response`);
    
    // Clear previous content
    parametersDiv.innerHTML = '';
    responseDiv.innerHTML = '';
    responseDiv.className = 'api-response';
    
    if (!apiKey) {
        descriptionDiv.style.display = 'none';
        executeDiv.style.display = 'none';
        return;
    }
    
    const apiInfo = APIs.get(apiKey);
    if (!apiInfo) return;
    
    
    // Show description
    descriptionDiv.innerHTML = apiInfo.description;
    descriptionDiv.style.display = 'block';
    
    // Create parameter inputs
    if (apiInfo.parameters) {
        Object.entries(apiInfo.parameters).forEach(([paramName, paramInfo]) => {
            const isRequired = apiInfo.required && apiInfo.required.includes(paramName);
            
            const paramDiv = document.createElement('div');
            paramDiv.className = 'parameter-group';
            
            paramDiv.innerHTML = `
                <label class="parameter-label ${isRequired ? 'required' : ''}">${paramName}</label>
                <input 
                    type="text" 
                    class="parameter-input ${isRequired ? 'required' : ''}"
                    placeholder="${paramInfo.description || `Enter ${paramName}`}"
                    data-param="${paramName}"
                    ${isRequired ? 'required' : ''}
                >
            `;
            
            parametersDiv.appendChild(paramDiv);
        });
    }
    
    // Show execute button
    executeDiv.style.display = 'block';
}

function convertStringFloatsToNumbers(obj) {
    /**
     * Recursively process object and convert string floats to numbers
     * Preserves .0 for whole numbers using toFixed(1)
     */
    if (typeof obj === 'string') {
        // Check if string looks like a float (e.g., "4241.0" or "123.456")
        if (/^-?\d+\.\d+$/.test(obj)) {
            // If it was a whole number with .0, format it
            if (obj.endsWith('.0')) {
                return parseFloat(obj).toFixed(1);
            } else{
                return parseFloat(obj);
            }
        }
        return obj;
    }
    if (Array.isArray(obj)) {
        return obj.map(convertStringFloatsToNumbers);
    }
    if (obj && typeof obj === 'object') {
        const converted = {};
        for (let key in obj) {
            converted[key] = convertStringFloatsToNumbers(obj[key]);
        }
        return converted;
    }
    return obj;
}

// function formatJSONWithFloats(obj, indent = 2) {
//     /**
//      * Custom JSON formatter that displays .0 for whole number floats
//      * without showing them as strings
//      */
//     const spaces = ' '.repeat(indent);
    
//     function format(value, depth = 0) {
//         const currentIndent = spaces.repeat(depth);
//         const nextIndent = spaces.repeat(depth + 1);
        
//         if (value === null) return 'null';
//         if (value === undefined) return 'undefined';
//         if (typeof value === 'boolean') return String(value);
//         if (typeof value === 'number') {
//             // Format whole numbers with .0
//             return Number.isInteger(value) ? `${value}.0` : String(value);
//         }
//         if (typeof value === 'string') {
//             // Check if it's a float string that should be displayed as number
//             if (/^-?\d+\.\d+$/.test(value)) {
//                 return value; // Display without quotes
//             }
//             return JSON.stringify(value);
//         }
//         if (Array.isArray(value)) {
//             if (value.length === 0) return '[]';
//             const items = value.map(item => `${nextIndent}${format(item, depth + 1)}`);
//             return `[\n${items.join(',\n')}\n${currentIndent}]`;
//         }
//         if (typeof value === 'object') {
//             const keys = Object.keys(value);
//             if (keys.length === 0) return '{}';
//             const items = keys.map(key => 
//                 `${nextIndent}"${key}": ${format(value[key], depth + 1)}`
//             );
//             return `{\n${items.join(',\n')}\n${currentIndent}}`;
//         }
//         return String(value);
//     }
    
//     return format(obj);
// }


async function executeAPI(actionId) {
    const environment = document.getElementById('environment').value.trim();
    const actionDiv = document.getElementById(actionId);
    const selectedRadio = actionDiv.querySelector('input[type="radio"]:checked');
    const selectedAPI = selectedRadio ? selectedRadio.value : null;
                
    if (!selectedAPI) {
        showWrongMessage('Please select an API first.');
        return;
    }
    
    // Collect parameters
    const parameters = {};
    const argumentFloatFields = []; // Track which arguments should preserve .0
    const paramInputs = actionDiv.querySelectorAll('.parameter-input');
    let hasError = false;
    
    paramInputs.forEach(input => {
        const paramName = input.dataset.param;
        let value = input.value.trim();
        const originalValue = value; // Store original for .0 detection
        
        if (value === '') {
            parameters[paramName] = value;
            return;
        }

        if (input.classList.contains('required') && !value) {
            input.style.borderColor = '#ff4757';
            hasError = true;
        } else {
            input.style.borderColor = '#e1e5e9';
            let parameterInfo = APIs.get(selectedAPI).parameters[paramName];
            
            // Check if original value was a number with .0 (before any parsing)
            // OR if it's a number type parameter that got converted to an integer
            if (/^\d+\.0$/.test(originalValue)) {
                argumentFloatFields.push(paramName);
            } else if (parameterInfo['type'] === 'number' && /^\d+$/.test(originalValue)) {
                // If it's a number type and user entered a whole number without decimal point,
                // we'll treat it as potentially needing .0 in export
                argumentFloatFields.push(paramName);
            }
            
            if (parameterInfo['type'] === 'object'){
                if (parameterInfo['properties'] !== undefined){
                    // Handle object properties
                    const properties = parameterInfo['properties'];
                    console.log('Parsing object for param:', paramName, typeof(value), value);
                    
                    try {
                        value = JSON.parse(value.replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false'));
                    } catch (e) {
                        console.error('Failed to parse JSON for param:', paramName, e);
                        showWrongMessage(`Invalid JSON format for parameter: ${paramName}. A JSON key must be enclosed by double quotes.`);
                        hasError = true;
                        return;
                    }
                    for (const v_key in value){
                        if (properties[v_key] !== undefined){
                            if (properties[v_key]['type'] === 'string'){
                                // Keep as string
                            }
                            else if (properties[v_key]['type'] === 'number'){
                                if (!Number.isNaN(Number(value[v_key]))){
                                    value[v_key] = Number(value[v_key]);
                                }
                            }
                            else if (properties[v_key]['type'] === 'boolean'){
                                const val = value[v_key];
                                if (typeof val === 'string') {
                                    const lower = val.toLowerCase();
                                    if (lower === 'true' || lower === 'false') {
                                        value[v_key] = lower === 'true';
                                    }
                                } else if (typeof val === 'boolean') {
                                    // Already a boolean, do nothing
                                } else {
                                    // Optional: handle invalid type
                                    console.warn(`Expected boolean or string, got: ${typeof val}`);
                                }
                            }
                            else if (properties[v_key]['type'] === 'array'){
                                try {
                                    value[v_key] = JSON.parse(value[v_key].replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false'));
                                    if (!Array.isArray(value[v_key])){
                                        throw new Error('Not an array');
                                    }
                                } catch (e) {
                                    // Invalid JSON, keep as string
                                }
                            }
                        }
                    }
                }
            }
            else{
                // Handle non-object types
                if (parameterInfo['type'] === 'string'){
                    // Keep as string
                }
                else if (parameterInfo['type'] === 'number'){
                    if (!Number.isNaN(Number(value))){
                        value = Number(value);
                    }
                }
                else if (parameterInfo['type'] === 'boolean'){
                    const val = value;
                    if (typeof val === 'string') {
                        const lower = val.toLowerCase();
                        if (lower === 'true' || lower === 'false') {
                            value = lower === 'true';
                        }
                    } else if (typeof val === 'boolean') {
                        // Already a boolean, do nothing
                    } else {
                        // Optional: handle invalid type
                        console.warn(`Expected boolean or string, got: ${typeof val}`);
                    }
                }
                else if (parameterInfo['type'] === 'array'){
                    try {
                        value = JSON.parse(value.replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false'));
                        if (!Array.isArray(value)){
                            throw new Error('Not an array');
                        }
                    } catch (e) {
                        // Invalid JSON, keep as string
                    }
                }
            }
            parameters[paramName] = value;
        }
    });
    
    if (hasError) {
        showWrongMessage('Please fill in all required fields.');
        return;
    }
    
    // Show loading state
    const executeButton = actionDiv.querySelector('.execute-button');
    const originalText = executeButton.textContent;
    executeButton.textContent = '⏳ Executing...';
    executeButton.disabled = true;
    
    const responseDiv = document.getElementById(`${actionId}_response`);
    responseDiv.innerHTML = '<div class="response-header">Executing API...</div>';
    responseDiv.className = 'api-response show';
    
    try {
        function fixNewlines(obj) {
            if (typeof obj === 'string') {
                return obj.replace(/\\n/g, '\n');
            }
            if (Array.isArray(obj)) {
                return obj.map(fixNewlines);
            }
            if (obj && typeof obj === 'object') {
                const fixed = {};
                for (let key in obj) {
                    fixed[key] = fixNewlines(obj[key]);
                }
                return fixed;
            }
            return obj;
        }

        const response = await fetch('/execute_api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                api_name: selectedAPI,
                parameters: parameters,
                environment: environment
            })
        });
        
        const result = await response.json();


        if (response.ok) {
            responseDiv.className = 'api-response show success';
            responseDiv.innerHTML = `
                <div class="response-header">✅ Success</div>
                <div class="response-content"><pre></pre><pre class="floatFields"></pre><pre class="argFloatFields" style="display:none;"></pre></div>
            `;
            // Set the JSON content as text to preserve literals
            
            // Process the data to convert literal \n to actual newlines
            console.log(result)
            try {
                result.output = JSON.parse(result.output)
            } catch (e) {
                // Not JSON, keep as is
            }
            // result.output = convertStringFloatsToNumbers(result.output)
            if (result.float_fields && Array.isArray(result.float_fields)) {
                result.output._floatFields = result.float_fields;
            }
            
            const displayResult = {
                output: result.output
            };
            const fixedResult = fixNewlines(displayResult);
            // console.log('Fixed Result:', fixedResult);
            responseDiv.querySelector('pre').textContent =  formatJSONWithFloats(fixedResult, 2, true);
            responseDiv.querySelector('.floatFields').textContent = result.float_fields ? `Float Fields: ${result.float_fields.join(', ')}` : '';
            // Store argument float fields for later export
            responseDiv.querySelector('.argFloatFields').textContent = argumentFloatFields.length > 0 ? argumentFloatFields.join(',') : '';
            showCorrectMessage('API executed successfully!');
        } else {
            responseDiv.className = 'api-response show error';
            responseDiv.innerHTML = `
                <div class="response-header">❌ Error</div>
                <div class="response-content">${JSON.stringify(result, null, 2)}</div>
            `;
            showWrongMessage('API execution failed. Check the response for details.');
        }
    } catch (error) {
        responseDiv.className = 'api-response show error';
        responseDiv.innerHTML = `
            <div class="response-header">❌ Network Error</div>
            <div class="response-content">Failed to connect to the server: ${error.message}</div>
        `;
        showWrongMessage('Network error occurred while executing the API.');
    } finally {
        executeButton.textContent = originalText;
        executeButton.disabled = false;
    }
}

function showCorrectMessage(text) {
    const message = document.createElement('div');
    message.textContent = text;
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #4caf50;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        font-family: Arial, sans-serif;
        transition: all 0.3s ease;
    `;
    document.body.appendChild(message);

    setTimeout(() => {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            document.body.removeChild(message);
        }, 300);
    }, 3000);
}

function showWrongMessage(text) {
    const message = document.createElement('div');
    message.textContent = text;
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #f44336;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        z-index: 1000;
        font-family: Arial, sans-serif;
        transition: all 0.3s ease;
    `;
    document.body.appendChild(message);

    setTimeout(() => {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            document.body.removeChild(message);
        }, 300);
    }, 3000);
}

function saveFilteredHTML() {
    // Clone the entire document
    const clonedDoc = document.cloneNode(true);

    // Sync input, textarea, and select values manually to clonedDoc
    const originalElements = document.querySelectorAll('input, textarea, select');
    const clonedElements = clonedDoc.querySelectorAll('input, textarea, select');

    originalElements.forEach((originalEl, index) => {
        const clonedEl = clonedElements[index];
        if (!clonedEl) return;

        switch (originalEl.tagName) {
            case 'TEXTAREA':
                clonedEl.innerHTML = originalEl.value;
                break;
            case 'SELECT':
                Array.from(clonedEl.options).forEach(option => {
                    option.removeAttribute('selected');
                    if (option.value === originalEl.value) {
                        option.setAttribute('selected', 'selected');
                    }
                });
                break;
            case 'INPUT':
                if (originalEl.type === 'checkbox' || originalEl.type === 'radio') {
                    if (originalEl.checked) {
                        clonedEl.setAttribute('checked', '');
                    } else {
                        clonedEl.removeAttribute('checked');
                    }
                } else {
                    clonedEl.setAttribute('value', originalEl.value);
                }
                break;
        }
    });

    // Remove unwanted elements
    const logo = clonedDoc.getElementById('image-logo');
    if (logo) logo.remove();

    // const elementsToExclude = clonedDoc.querySelectorAll('.save-button');
    // elementsToExclude.forEach(el => el.remove());

    const formTitle = clonedDoc.querySelector('main.content-area .form-title');
    if (formTitle) formTitle.remove();

    const formTextarea = clonedDoc.querySelector('main.content-area .form-textarea');
    if (formTextarea) formTextarea.remove();

    const queryBtn = clonedDoc.querySelector('main.content-area .query-btn');
    if (queryBtn) queryBtn.remove();

    // Save as an HTML file
    const htmlContent = '<!DOCTYPE html>\n' + clonedDoc.documentElement.outerHTML;
    const blob = new Blob([htmlContent], { type: 'text/html' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'filtered_page.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);

    URL.revokeObjectURL(url);
    showCorrectMessage('Page saved successfully!');
}
/////////////////////////////////////////////
env = null;
model_provider = null;
model = null;
num_trials = null;
temperature = null;
interface_num = null;
edgesBefore = null; // so as not to conflict with graph edges
user_id = null;
instruction = null;
actionsBefore = null;
////////////////////////////////////////////
// taskBefore_text = null;


function importActions() {
    const input = document.getElementById('fileInput');
    input.value = '';
    input.click();
    input.onchange = () => {
        const file = input.files[0];
        const reader = new FileReader();
        reader.onload = e => {
            
            try {
                // taskBefore = e.target.result
                // console.log('File content:', taskBefore);
                const obj = JSON.parse(e.target.result);
                env = obj["env"]
                model_provider = obj["model_provider"]
                model = obj["model"]
                num_trials = obj["num_trials"]
                temperature = obj["temperature"]
                interface_num = obj["interface_num"]
                if (obj["task"]) {
                    user_id = obj["task"]["user_id"]
                    instruction = obj["task"]["instruction"]
                    actionsBefore = obj["task"]["actions"]
                    edgesBefore = obj["task"]["edges"]
                } else{
                    user_id = obj["task"]
                    instruction = obj["task"]
                    actionsBefore = obj["actions"]
                    edgesBefore = obj["edges"]
                }

                console.log('Imported actions:', obj);
                // const added = new Set();
                let imported_actions = obj.actions;
                let actions_interface = obj.interface_num;
                if (!obj.actions || !Array.isArray(obj.actions)) {
                    imported_actions = obj.task.actions;
                    // actions_interface = obj.task.interface_num;
                }
                var environment_selected = document.getElementById("environment");
                if (env && environment_selected.value.trim() !== env) {
                    // environment_selected.value = env;
                    showWrongMessage(`The imported task is for the environment: ${env} whereas the current environment is: ${environment_selected.value.trim()}. Please change the environment first.`);
                    return;
                }

                var interface_selected = document.getElementsByClassName("form-select")[0];
                var interface_selected_text = interface_selected.options[interface_selected.selectedIndex].text;
                interface_selected_text = interface_selected_text.split(' ')[1];
                // console.log(interface_selected_text, actions_interface);
                if (actions_interface && parseInt(actions_interface) !== parseInt(interface_selected_text)) {
                    showWrongMessage(`The imported actions are for the interface: ${actions_interface} whereas the environment is using interface: ${interface_selected_text}. Please select the correct interface first.`);
                    return;
                }

                imported_actions.forEach(action => {
                    // if (added.has(action.name)) return;
                    // added.add(action.name);
                    [actionID, actionDiv] = addAction();
                    if (actionID === null || actionDiv === null) return;
                    const radioButton = actionDiv.querySelector(`input[type="radio"][value="${action.name}"]`);
                    if (radioButton) {
                        radioButton.checked = true;
                    }
                    selectAPI(actionID, action.name);
                    actionDiv.querySelectorAll('.parameter-input').forEach(input => {
                        const paramName = input.dataset.param;
                        let value = action.arguments[paramName];
                        if (value !== undefined) {
                            // Check if value is a non-null object (but not an array or Date)
                            if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
                                try {
                                    value = JSON.stringify(value);
                                } catch (e) {
                                    console.warn(`Failed to stringify value for ${paramName}`, e);
                                }
                            }
                            input.value = value;
                        }
                    });
                    // console.log('Action ID:', actionID);
                });
            } catch (error) {
                console.error('Error importing actions:', error);
                showWrongMessage('Failed to import actions. Please check the file format.');
            }
        };
        reader.readAsText(file);
    };
}

function getTaskActions(catchFloat = true){
    const actions = [];
    const actionElements = document.querySelectorAll('.api-action');
    
    actionElements.forEach(actionEl => {
        const selectedRadio = actionEl.querySelector('input[type="radio"]:checked');
        const selectedAPI = selectedRadio ? selectedRadio.value : null;
        
        if (!selectedAPI) return;
        
        const parameters = new Map();
        const paramInputs = actionEl.querySelectorAll('.parameter-input');
        
        paramInputs.forEach(input => {
            const paramName = input.dataset.param;
            let value = input.value.trim();
            const originalValue = value;
            if (value.startsWith('{') || value.startsWith('[')) {
                try {
                    value = JSON.parse(value.replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false'));
                    // parameters.set(paramName, JSON.parse(fixedVal));
                } catch (e) {
                    // parameters.set(paramName, paramVal);
                }
            }

            if (input.classList.contains('required') && !value) {
                input.style.borderColor = '#ff4757';
                hasError = true;
            } else {
                input.style.borderColor = '#e1e5e9';
                let parameterInfo = APIs.get(selectedAPI).parameters[paramName];
                if (parameterInfo['type'] === 'object'){
                    if (parameterInfo['properties'] !== undefined){
                        // Handle object properties
                        const properties = parameterInfo['properties'];
                        // console.log('Parsing object for param:', paramName, typeof(value), value);
                        if (value === '') {
                            value = {};
                        }
                        // try {
                        //     value = JSON.parse(value.replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false'));
                        // } catch (e) {
                        //     console.error('Failed to parse JSON for param:', paramName, e);
                        //     showWrongMessage(`Invalid JSON format for parameter: ${paramName}. A JSON key must be enclosed by double quotes.`);
                        //     hasError = true;
                        //     return;
                        // }
                        for (const v_key in value){
                            if (properties[v_key] !== undefined){
                                if (properties[v_key]['type'] === 'string'){
                                    // Keep as string
                                }
                                else if (properties[v_key]['type'] === 'number'){
                                    if (!Number.isNaN(Number(value[v_key]))){
                                        value[v_key] = Number(value[v_key]);
                                    }
                                }
                                else if (properties[v_key]['type'] === 'boolean'){
                                    const val = value[v_key];
                                    if (typeof val === 'string') {
                                        const lower = val.toLowerCase();
                                        if (lower === 'true' || lower === 'false') {
                                            value[v_key] = lower === 'true';
                                        }
                                    } else if (typeof val === 'boolean') {
                                        // Already a boolean, do nothing
                                    } else {
                                        // Optional: handle invalid type
                                        console.warn(`Expected boolean or string, got: ${typeof val}`);
                                    }
                                }
                                else if (properties[v_key]['type'] === 'array'){
                                    try {
                                        value[v_key] = JSON.parse(value[v_key].replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false'));
                                        if (!Array.isArray(value[v_key])){
                                            throw new Error('Not an array');
                                        }
                                    } catch (e) {
                                        // Invalid JSON, keep as string
                                    }
                                }
                            }
                        }
                    }
                }
                else{
                    // Handle non-object types
                    if (parameterInfo['type'] === 'string'){
                        // Keep as string
                    }
                    else if (parameterInfo['type'] === 'number'){
                        if (!Number.isNaN(Number(value))){
                            value = Number(value);
                        }
                    }
                    else if (parameterInfo['type'] === 'boolean'){
                        const val = value;
                        if (typeof val === 'string') {
                            const lower = val.toLowerCase();
                            if (lower === 'true' || lower === 'false') {
                                value = lower === 'true';
                            }
                        } else if (typeof val === 'boolean') {
                            // Already a boolean, do nothing
                        } else {
                            // Optional: handle invalid type
                            console.warn(`Expected boolean or string, got: ${typeof val}`);
                        }
                    }
                    else if (parameterInfo['type'] === 'array'){
                        try {
                            value = JSON.parse(value.replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false'));
                            if (!Array.isArray(value)){
                                throw new Error('Not an array');
                            }
                        } catch (e) {
                            // Invalid JSON, keep as string
                        }
                    }
                }
                if (value !== '') {
                    parameters.set(paramName, value);
                }
            }
        });

        // paramInputs.forEach(input => {
        //     const paramName = input.dataset.param;
        //     let paramVal = input.value.trim();
        //     if (paramVal !== '') {
        //         if (!Number.isNaN(Number(paramVal)) && !paramName.includes('phone') && !paramName.includes('mobile')) {
        //             if (paramName.includes('_id') || paramName.includes('_by') || paramName.includes('_to') || paramName === 'name' || paramName === 'new_value' || paramName === 'old_value' || paramName.includes('phone') || paramName.includes('mobile')) {
        //                 parameters.set(paramName, paramVal);
        //             } else {
        //                 parameters.set(paramName, Number(paramVal));
        //             }
        //         } else if (paramVal.toLowerCase() === 'true' || paramVal.toLowerCase() === 'false') {
        //             paramVal = paramVal.toLowerCase();
        //             parameters.set(paramName, (paramVal === 'true'));
        //         } else if (paramVal.startsWith('{') || paramVal.startsWith('[')) {
        //             try {
        //                 const fixedVal = paramVal.replace(/\bTrue\b/g, 'true').replace(/\bFalse\b/g, 'false');
        //                 parameters.set(paramName, JSON.parse(fixedVal));
        //             } catch (e) {
        //                 parameters.set(paramName, paramVal);
        //             }
        //         } else {
        //             parameters.set(paramName, paramVal);
        //         }
        //     }
        // });
        console.log(parameters);
        let output = '';
        const outputContent = actionEl.querySelector('.response-content pre');
        const floatFieldsContent = actionEl.querySelector('.response-content pre.floatFields');
        const argFloatFieldsContent = actionEl.querySelector('.response-content pre.argFloatFields');
        let argFloatFields = [];
        if (argFloatFieldsContent && argFloatFieldsContent.textContent.trim()) {
            argFloatFields = argFloatFieldsContent.textContent.split(',').filter(f => f);
        }
        if (outputContent) {
            let text = outputContent.textContent.trim();
            // console.log('Raw text:', text); // DEBUG
            
            try {
                const parsed = JSON.parse(text);
                output = parsed.hasOwnProperty('output') ? parsed.output : parsed;
                // console.log('Parsed output:', output); // DEBUG
                
                // Extract float fields from the separate pre element
                if (catchFloat && floatFieldsContent && floatFieldsContent.textContent.trim()) {
                    const floatFieldsText = floatFieldsContent.textContent.trim();
                    const match = floatFieldsText.match(/Float Fields: (.+)/);
                    if (match) {
                        const floatFieldsArray = match[1].split(',').map(f => f.trim()).filter(f => f);
                        if (floatFieldsArray.length > 0) {
                            if (typeof output === 'object' && output !== null) {
                                output._floatFields = floatFieldsArray;
                            }
                        }
                    }
                }
                // console.log('Float fields:', output._floatFields); // DEBUG
            } catch (e) {
                console.error('Error parsing output:', e);
                output = '';
            }
        }
        
        let sortedOutput = output;
        if (output && typeof output === 'object' && !Array.isArray(output)) {
            sortedOutput = {};
            const outputEntries = Object.entries(output);
            outputEntries.sort((a, b) => a[0].localeCompare(b[0]));
            outputEntries.forEach(([key, value]) => {
                sortedOutput[key] = value;
            });
        }

        const actionData = {
            name: selectedAPI,
            arguments: Object.fromEntries(parameters),
            output: output
        };

        if (argFloatFields.length > 0) {
            actionData.arguments._floatFields = argFloatFields;
        }

        actions.push(actionData);
    });
    
    // console.log('Final actions:', actions); // DEBUG
    return actions;
}


function formatJSONWithFloats(obj, indent = 2, removeFloatFields = false) {
    const spaces = ' '.repeat(indent);
    
    function format(value, depth = 0, currentKey = '', floatFields = new Set()) {
        const currentIndent = spaces.repeat(depth);
        const nextIndent = spaces.repeat(depth + 1);
        
        if (value === null) return 'null';
        if (value === undefined) return 'undefined';
        if (typeof value === 'boolean') return String(value);
        if (typeof value === 'number') {
            if (Number.isInteger(value) && floatFields.has(currentKey)) {
                return `${value}.0`;
            }
            return String(value);
        }
        if (typeof value === 'string') {
            // Only treat numeric strings as unquoted numbers if they're in floatFields
            if (/^-?\d+\.\d+$/.test(value) && floatFields.has(currentKey)) {
                return value;
            }
            return JSON.stringify(value);
        }
        if (Array.isArray(value)) {
            if (value.length === 0) return '[]';
            // For arrays, pass the floatFields through so nested objects can use them
            const items = value.map(item => `${nextIndent}${format(item, depth + 1, currentKey, floatFields)}`);
            return `[\n${items.join(',\n')}\n${currentIndent}]`;
        }
        if (typeof value === 'object') {
            let localFloatFields = new Set(floatFields);
            if (value._floatFields && Array.isArray(value._floatFields)) {
                value._floatFields.forEach(f => localFloatFields.add(f));
            }
            
            // Filter out _floatFields if removeFloatFields is true
            let entries = Object.entries(value).filter(([k, v]) => !removeFloatFields || k !== '_floatFields');
            
            if (entries.length === 0) return '{}';
            const items = entries.map(([key, val]) => 
                // Pass the actual key name so nested values can check against floatFields
                `${nextIndent}"${key}": ${format(val, depth + 1, key, localFloatFields)}`
            );
            return `{\n${items.join(',\n')}\n${currentIndent}}`;
        }
        return String(value);
    }
    
    return format(obj, 0, '');
}

function exportActions() {
    const actions = getTaskActions();
    const exportData = { actions: actions };
    const jsonStr = formatJSONWithFloats(exportData, 2, true);
    
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'actions.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}