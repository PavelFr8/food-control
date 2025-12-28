import os
from typing import Any

from dotenv import load_dotenv


load_dotenv(override=False, dotenv_path="../.env")


def get_env(var_name: str, default: Any, cast: type):
    value = get_casted_value(var_name, cast)
    if value is None:
        return default

    return value


def get_casted_value(var_name: str, cast: type):
    value = os.environ.get(var_name)
    if value is None:
        return None

    if cast == list:
        return value.split(",")

    if cast == bool:
        return value.lower().strip() in ["1", "true", "yes", "y", ""]

    return cast(value)
