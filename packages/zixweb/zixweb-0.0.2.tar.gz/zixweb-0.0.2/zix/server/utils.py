import os
import sys
from types import ModuleType
from typing import Dict

import yaml


def is_local() -> bool:
    return os.environ.get("DOMAIN") in [None, "localhost"]


def str_to_bool(string:str,) -> str:
    if not string:
        return None
    return string.lower() in ["true", "t"]


def list_submodules(module: ModuleType) -> Dict:
    submodules = dict()
    objects = dir(module)
    for name in objects:
        if name[0] == "_":
            continue
        obj = getattr(module, name)

        if not callable(obj):
           submodules[name] = obj
    return submodules


def dynamic_import(
        path:str,
        module_name:str,
        module_globals=None,
        ) -> ModuleType:
    """ Dynamically import module """
    sys.path.insert(1, path)
    kwargs = dict(globals=module_globals) if module_globals else {}
    module = __import__(module_name, **kwargs)
    return module


def import_submodules(
        path:str,
        parent_module: str,
        ) -> ModuleType:
    parent_path = os.path.join(path, "..")
    for submodule in os.listdir(os.path.join(path, parent_module)):
        if submodule == "__init__.py":
            continue
        if (os.path.isdir(os.path.join(path, parent_module, submodule)) and
            os.path.exists(os.path.join(path, parent_module, submodule, "__init__.py")) and
            not os.path.exists(os.path.join(path, parent_module, submodule, ".zixignore"))):
            module = dynamic_import(parent_path, parent_module + "." + submodule)
    return module


def define_env_vars_from_yaml(
    yaml_file:str,
    stage: str="local",
    ) -> None:
    """
    Read a yaml file with the following format to define the environment variables

    ```
    prod:
        <ENV_VAR_KEY>: <string value>
    <stage_name>:
        <ENV_VAR_KEY>: <string value>
    local:
        <ENV_VAR_KEY>: <string value>
    ```

    Example:
    ```
    local:
        API_KEY: xxxyyy01234
    ```
    """
    with open(yaml_file, "r") as f:
        stages = yaml.load(f, Loader=yaml.FullLoader)
    envs = stages[stage]
    for key in envs.keys():
        os.environ[key] = str(envs[key])
