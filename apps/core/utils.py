from importlib import import_module
from pathlib import Path


def auto_import_dir_modules(app_name: str, file: str):
    """
    Import all .py files in the directory (except __init__.py and _*.py),
    using the given Django app name and current folder name.

    Args:
        app_name (str): Dotted Python path to the app (e.g., 'apps.ecommerce')
        file (str): __file__ of the calling module
    """
    directory = Path(file).parent
    subfolder_name = directory.name
    full_module_path = f"{app_name}.{subfolder_name}"

    for py_file in directory.glob("*.py"):
        if py_file.name != "__init__.py" and not py_file.name.startswith("_"):
            module_name = py_file.stem
            import_module(f"{full_module_path}.{module_name}")
