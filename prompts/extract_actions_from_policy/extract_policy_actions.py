

prompt = """
You are an expert in extracting policy actions from a given text. Your task is to analyze the provided policies and extract all the actions/APIs related to policies. Each action should be clearly defined and categorized based on its type (e.g., create, update, delete, get).

Look at the following examples of policy actions:
{actions}

Your job is to extract similar actions from the provided policy text. Ensure that you capture all relevant details such as action name, description, and any parameters associated with the action.
Here is the policy text from which you need to extract actions:
{policy_text}
"""

def create_policy_actions_prompt():
    with open('examples_policy_actions.txt', 'r') as f:
        actions = f.read()
    with open('policy.txt', 'r') as f:
        policy_text = f.read()
    
    return prompt.format(actions=actions, policy_text=policy_text)


returned_prompt = create_policy_actions_prompt()

with open('created_policy_actions_prompt.txt', 'w') as f:
    f.write(returned_prompt)
