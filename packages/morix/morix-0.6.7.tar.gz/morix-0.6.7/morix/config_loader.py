import os
import yaml
import shutil
import logging
from .version import PROGRAM_NAME
from typing import Dict, Any

logger = logging.getLogger(__name__)

CONFIG_LOCAL_DIR = 'configs'
CONFIG_HOME_DIR = '.config'
CONFIG_YAML = 'config.yml'
CONFIG_FUNCTIONS = 'functions.yml'
CONFIF_IGNORE_FILE = '.gptignore'

def get_config_folder():
    if is_development_mode():
        config_dir = os.path.join(os.path.dirname(__file__), CONFIG_LOCAL_DIR)
    else:
        config_dir = os.path.join(os.path.expanduser('~'), CONFIG_HOME_DIR, PROGRAM_NAME)
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


def load_config() -> Dict[str, Any]:
    config_dir = get_config_folder()
    return load_yaml(config_dir, CONFIG_YAML)


def open_config_file() -> None:
    config_path = os.path.join(get_config_folder(), CONFIG_YAML)

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

def check_config_files():
    # if not is_development_mode():
    home_dir = os.path.expanduser('~')
    config_dir = os.path.join(home_dir, CONFIG_HOME_DIR, PROGRAM_NAME)
    templates_dir = os.path.join(os.path.dirname(__file__), CONFIG_LOCAL_DIR)
    config_files = [f for f in os.listdir(templates_dir) if os.path.isfile(os.path.join(templates_dir, f))]

    if not os.path.exists(config_dir):
        print(f"Creating configuration directory at {config_dir}")
        os.makedirs(config_dir)

    for config_file in config_files:
        template_path = os.path.join(templates_dir, config_file)
        target_path = os.path.join(config_dir, config_file)

        if not os.path.exists(template_path):
            continue

        if not os.path.exists(target_path):
            print(f"Add {config_file} to {config_dir}")
            shutil.copy(template_path, target_path)

    logger.info(f"Configuration copied to {config_dir}")

class Config:
    def __init__(self):
        check_config_files()
        self.path = get_config_folder()
        self.config_data = load_yaml(self.path, CONFIG_YAML)
        self.gpt_model = self.config_data.get('gpt_model')
        self.log_level = self.config_data.get('log_level')
        self.ignore_pattern_files = self.config_data.get('ignore_pattern_files')
        self.text_extensions = self.config_data.get('text_extensions')
        self.functions = self.config_data.get('functions')
        self.role = self.config_data.get('role')
        self.permissions = self.config_data.get('permissions')
        self.command_output = self.config_data.get('command_output', {'max_output_lines': 100})
        self.role_system_content = self.role['system']['developer']['content']
        self.additional_user_content = self.role['user']['additional_content']
        self.default_functions = load_yaml(self.path, CONFIG_FUNCTIONS)
        self.plugins_path = f"{self.path}/plugins"


config = Config()