import re

class_defaults = {
    'doClear': True,
    'allowDev': False,
    'allowMods': False,
    'checkVersion': True,
    'saveCFG': True,
    'loadCFG': True
}

with open('example.py', 'r') as file:
    content = file.read()

for key, value in class_defaults.items():
    pattern = rf'{key}: bool = (True|False)'
    replacement = f'{key}: bool = {value}'
    content = re.sub(pattern, replacement, content)

with open('example.py', 'w') as file:
    file.write(content)