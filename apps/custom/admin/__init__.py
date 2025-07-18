from apps.core.utils import auto_import_dir_modules

from ..apps import APP_NAME

auto_import_dir_modules(APP_NAME, __file__)

# * This file is used to automatically import all modules in the current directory.
