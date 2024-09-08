import os
import sys
import logging
from typing import Any, Dict, List
from venv import logger
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from .config_loader import config
import tiktoken


def get_string_size_kb(string: str) -> float:
    size_bytes = len(string.encode('utf-8'))
    size_kb = size_bytes / 1024
    return size_kb


def save_response_to_file(response: str, temp_dir: str) -> str:
    count = len(os.listdir(temp_dir)) + 1
    file_path = os.path.join(temp_dir, f"response_{count}.md")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response)
        logger.info(f"Response saved in {temp_dir}")
    except IOError as e:
        logger.error(f"Error saving response to file: {file_path}: {e}", exc_info=True)
    return file_path


style = Style.from_dict({
    'prompt': 'ansiblue bold',
})


bindings = KeyBindings()


@bindings.add('c-c')
def _(event):
    exit()


@bindings.add('c-d')
def _(event):
    exit()


@bindings.add('enter')
def _(event):
    buffer = event.current_buffer
    if buffer.validate():
        buffer.validate_and_handle()


def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except IOError as e:
        logger.error(f"Failed to read file {file_path}: {e}", exc_info=True)
        return ""


def num_tousend_tokens_from_messages(messages: List[Dict[str, Any]], model: str = config.gpt_model):
    """Returns the number of thousand tokens in messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("Model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0

    for message in messages:
        if isinstance(message, dict):
            for _, value in message.items():
                if isinstance(value, str):  # Check if the value is a string
                    try:
                        num_tokens += len(encoding.encode(value, disallowed_special=()))
                    except:
                        logger.error(f"Error encoding value: {value}")
        else:
            try:
                num_tokens += len(encoding.encode(str(message), disallowed_special=()))
            except:
                logger.error(f"Error encoding object: {message}")

    # Round up to the nearest thousand tokens
    tokens_per_thousand = (num_tokens + 999) // 1000
    logger.info(f"Message contains ~{max(1, tokens_per_thousand)}K tokens")


def set_marker():
    sys.stdout.write('\x1b[s')


def clear_to_marker():
    sys.stdout.write('\x1b[u')  # Return to the saved cursor position
    sys.stdout.write('\x1b[J')  # Clear everything below the cursor


def check_git_presence(work_folder: str) -> None:
    if not os.path.exists(os.path.join(work_folder, ".git")):
        logger.warning("Warning: No .git directory found in the working directory.")
        input("Press Enter to continue...")

# def merge_functions_describes():
#     try:
#         if os.path.exists(os.path.join(scan_folder, "functions.yml")):
#             project_functions = load_yaml(scan_folder, "functions.yml")
#             merged_functions = config.default_functions + project_functions
#             return merged_functions
#     except Exception as e:
#         logger.error(f"Error loading functions from {scan_folder}: {e}")

#     return config.default_functions
