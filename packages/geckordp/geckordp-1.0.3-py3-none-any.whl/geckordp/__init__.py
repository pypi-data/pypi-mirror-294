import os

import geckordp.settings
from geckordp.settings import *

# pylint: disable=invalid-name


# check if environment variables are set and override it
VAR_ID = "_Settings__X"
for name, value in GECKORDP.__dict__.items():
    # check if correct variable
    if not name.startswith(VAR_ID):
        continue

    # get required variables
    func_name = name.replace(VAR_ID, "")
    env_name = name.replace(VAR_ID, "GECKORDP_")
    env_value = os.environ.get(env_name, None)

    # check if environment variable was set
    if env_value is None:
        continue

    # try to convert value to class variable type
    try:
        env_value = type(value)(env_value)
    except Exception as ex:
        print(f"invalid type for environment variable '{env_name}':\n{ex}")
        continue

    # change value by calling setter property
    try:
        func = getattr(Settings, func_name)
        func.fset(GECKORDP, env_value)
    except Exception as ex:
        print(f"env-set: {ex}")
