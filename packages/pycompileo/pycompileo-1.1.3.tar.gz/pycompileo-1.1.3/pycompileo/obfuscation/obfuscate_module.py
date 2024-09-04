import os
import sys
from ..compilation import compile


def generate_init_loader(filename: str):
    return f'''import {filename}'''


def obfuscate_module(path: str, output_path=None, syspath: str = None):
    if syspath:
        sys.path.insert(1, syspath)

    assert os.path.exists(path), Exception('File does not exist.')

    if not output_path:
        output_path = f'./c{path}'

    compile(path, output_path)
