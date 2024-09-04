import sys

from ..schemas.events import LoadedModules


def get_loaded_modules() -> LoadedModules:
    loaded_modules = []

    # TODO: Might wanna use importlib.resources added in 3.7
    for module_name, module in sys.modules.items():
        version = getattr(module, "__version__", None)
        if version:
            version = str(version)
        loaded_modules.append(LoadedModules.ModuleData(module_name, version))
    return LoadedModules(loaded_modules)
