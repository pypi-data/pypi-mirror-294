import os
import yaml
import logging
from .version import PROGRAM_NAME
from typing import Tuple, Dict, Any

logger = logging.getLogger(__name__)


def get_config_folder():
    if is_development_mode():
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        config_dir = os.path.join(parent_dir, 'templates')
    else:
        config_dir = os.path.join(os.path.expanduser('~'), '.config', PROGRAM_NAME)
    return config_dir

def load_yaml(config_dir, file_name):
    config_path = os.path.join(config_dir, file_name)
    if not os.path.exists(config_path):
        logger.error(f"File {file_name} not found at path: {config_path}")
        raise FileNotFoundError(f"File {file_name} not found at path: {config_path}")

    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Error loading {file_name}: {e}", exc_info=True)
        raise

def load_config() -> Tuple[Dict[str, Any]]:
    config_dir = get_config_folder()
    return load_yaml(config_dir, "config.yml")


def open_config_file() -> None:
    config_path =  os.path.join(get_config_folder(), "config.yml")

    if config_path:
        os.system(f'open "{config_path}"' if os.name == 'posix' else f'start "" "{config_path}"')
    else:
        logger.error("Configuration file not found.")

def is_development_mode() -> bool:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    res = os.path.isfile(os.path.join(parent_dir, 'setup.py'))
    if res:
        logger.debug("Running in development mode")
    return res

config_path = get_config_folder()
config = load_config()
default_functions = load_yaml(config_path, "functions.yml")
gpt_model = config['gpt_model']
role = config['role']
role_system_content = role['system']['developer']['content']
additional_user_content = role['user']['additional_content']
log_level = config['log_level']
