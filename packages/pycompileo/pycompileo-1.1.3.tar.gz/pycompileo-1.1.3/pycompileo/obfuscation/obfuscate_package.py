import os
import sys
from ..compilation import compile


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


def obfuscate_package_fake_init(path: str, output_path=None, syspath: str = None):
    if syspath:
        sys.path.insert(1, syspath)

    assert os.path.exists(path), Exception('Folder does not exist.')

    folder_name = os.path.basename(path)

    if not output_path:
        output_path = f'c{folder_name}'

    # os.rename(folder_path, f"old_{folder_name}")

    compile(folder_name, f"{output_path}/internal")

    with open(f'{output_path}/__init__.py', 'w') as f:
        f.write(generate_init_loader(f'{output_path}'))


def obfuscate_package(path: str, output_path=None, syspath: str = None):
    if syspath:
        sys.path.insert(1, syspath)

    assert os.path.exists(path), Exception('Folder does not exist.')

    folder_name = os.path.basename(path)

    if not output_path:
        output_path = f'c{folder_name}'

    # os.rename(folder_path, f"old_{folder_name}")

    compile(folder_name, f"{output_path}")

    # with open(f'{new_folder_name}/__init__.py', 'w') as f:
    #     f.write(generate_init_loader(f'{new_folder_name}'))
