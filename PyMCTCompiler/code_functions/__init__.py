import os
import glob
from typing import Dict
import shutil

print("Loading Code Primitives ...")
code_primitives: Dict[str, str] = {}
used_code_primitives = set()

for f_path in glob.iglob(
    os.path.join(os.path.dirname(__file__), "data", "**", "*.py"), recursive=True
):
    f = os.path.basename(f_path)
    primitive_name = os.path.splitext(f)[0]
    if primitive_name in code_primitives:
        print(f'code primitive "{primitive_name}" is defined twice')
    with open(f_path) as l:
        code_primitives[primitive_name] = l.read()

print("\tFinished Loading Code Primitives")


def _recursive_to_tuple(data):
    if isinstance(data, list):
        return tuple(_recursive_to_tuple(d) for d in data)
    else:
        return data


def get(code_function_name) -> None:
    assert (
        code_function_name in code_primitives
    ), f'Code function "{code_function_name}" does not exist'
    used_code_primitives.add(code_function_name)


def save(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)
    with open(os.path.join(path, "__init__.py"), "w") as l_:
        pass
    for code_function_name in used_code_primitives:
        code_function = code_primitives[code_function_name]
        with open(os.path.join(path, f"{code_function_name}.py"), "w") as l_:
            l_.write(code_function)
