import importlib.util
import sys


def decompile(path, module_name="module_name", syspath: str = None, runsyspath: str = None):
    """ Module name is required for unobfuscating folders. """
    if syspath:
        sys.path.insert(1, syspath)

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)

    if syspath:
        sys.path.remove(sys.path[1])

    if runsyspath:
        sys.path.insert(1, runsyspath)

    spec.loader.exec_module(module)

    return module
