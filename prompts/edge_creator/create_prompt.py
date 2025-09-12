
with open('instructions.txt', 'r') as file:
    instructions = file.read()

with open('examples.txt', 'r') as file:
    examples = file.read()

with open('actions.txt', 'r') as file:
    actions = file.read()
print(instructions)

prompt = instructions.format(examples=examples, actions=actions)

with open('create_edge_prompt.txt', 'w') as file:
    file.write(prompt)