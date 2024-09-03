import os
from ..utility import obfuscate


def generate_init_loader(libname: str):
    return f'''import sys
import os
import pycompileo as ob

total_working_dir = os.path.join(os.getcwd(), '{libname}')

sys.path.append(total_working_dir)
compiled_module = ob.unobfuscate(f'{libname}/internal/__init__.pyc', 'internal')

# Dump everything in the module to the global namespace
for attribute in dir(compiled_module):
    if not attribute.startswith('__'):
        globals()[attribute] = getattr(compiled_module, attribute)
'''


def obfuscate_module(folder_path: str, new_folder_name=None):
    assert os.path.exists(folder_path), Exception('Folder does not exist.')

    folder_name = os.path.basename(folder_path)

    if not new_folder_name:
        new_folder_name = f'c{folder_name}'

    # os.rename(folder_path, f"old_{folder_name}")

    obfuscate(folder_name, f"{new_folder_name}/internal")

    with open(f'{new_folder_name}/__init__.py', 'w') as f:
        f.write(generate_init_loader(f'{new_folder_name}'))
