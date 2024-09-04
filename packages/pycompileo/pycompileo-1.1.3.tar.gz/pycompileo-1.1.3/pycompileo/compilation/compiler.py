import os
import py_compile
import sys
import shutil


def compile_file(path: str, output_path: str):
    if os.path.isdir(output_path) and not os.path.isfile(output_path):
        filename = os.path.basename(path)
        output_path = os.path.join(output_path, filename)

    pyc_path = f'{output_path}c'
    py_compile.compile(path, cfile=pyc_path, optimize=0)
    print(f"Compiled file: {path} to {pyc_path}")


def compile_directory(path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, path)
            output_file = os.path.join(output_dir, rel_path)

            os.makedirs(os.path.dirname(output_file), exist_ok=True)

            if file.endswith('.py'):
                output_file += 'c'
                py_compile.compile(file_path, cfile=output_file, optimize=0)
                print(f"Compiled file: {file_path} to {output_file}")
            else:
                shutil.copy(file_path, output_file)
                print(f"Copied file: {file_path} to {output_file}")


def compile(path: str,
            output_dir: str = 'compiled_files',  # Directory name to store compiled package
            output_file: str = 'compiled_file.py',    # File name to store compiled python file
            syspath: str = None):

    if syspath:
        sys.path.insert(1, syspath)

    if os.path.isfile(path):
        compile_file(path, output_dir)
    elif os.path.isdir(path):
        compile_directory(path, output_dir)
    else:
        raise Exception(f"The path {path} is neither a file nor a directory or does not exist.")
