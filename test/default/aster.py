import ast

with open('example.py', 'r') as file:
    tree = ast.parse(file.read())

class_defaults = {
    'doClear': True,
    'allowDev': False,
    'allowMods': False,
    'checkVersion': True,
    'saveCFG': True,
    'loadCFG': True
}

for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef) and node.name == 'devCFG':
        print("Checking class devCFG")
        for attr in node.body:
            if isinstance(attr, ast.AnnAssign):
                if attr.target.id in class_defaults:
                    default = class_defaults[attr.target.id]
                    attr.value = ast.Constant(default)
                    print(f'Defaulted attribute "{attr.target.id}" to {default}')

with open('example.py', 'w') as file:
    file.write(ast.unparse(tree))