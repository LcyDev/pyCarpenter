import os

def CLS(new_line=True):
    if DEBUG: return
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    if new_line: print()

def addStrIf(iterable: list, string: str, check: bool):
    if check: iterable.append(string)

def joinIfStr(iterable: list, body: str, string: str):
    if string: iterable.append(body + f'"{string}"')

def extIfStr(iterable: list, string: str, other: list):
    iterable.extend([string + f'"{i}"' for i in other if i])