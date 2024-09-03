import importlib.util


def unobfuscate(path, module_name="module_name"):
    """ Module name is required for unobfuscating folders. """
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(module)

    return module
