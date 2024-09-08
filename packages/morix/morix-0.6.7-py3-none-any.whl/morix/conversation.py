import os
import logging
from venv import logger
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console
from prompt_toolkit import prompt
from colorama import init

from .functions import process_tool_calls
from .scan import scan, get_project_structure
from .helpers import clear_to_marker, get_string_size_kb, bindings, set_marker, style, num_tousend_tokens_from_messages
from .config_loader import config
from .complection import chat_completion_request

# Initialize colorama for Windows
init()

console = Console()

logger = logging.getLogger(__name__)

def scan_folder(scan_folder: str, need_scan: bool, structure_only: bool) -> str:
    if not need_scan:
        return ""
    if structure_only:
        return get_project_structure(scan_folder)
    else:
        scan_result = scan(scan_folder)
        logger.debug(f"Scanning completed. Size in kilobytes: {get_string_size_kb(scan_result):.2f} KB.")
        return scan_result


def initialize_messages(scan_result: str, work_folder: str, initial_message: str = None) -> list:
    messages = []
    # merge_functions(work_folder)

    if config.role_system_content:
        messages.append({"role": "system", "content": config.role_system_content})
        console.print(Panel(config.role_system_content, title="[green]System Message[/green]"))

    if config.additional_user_content:
        messages.append({"role": "user", "content": config.additional_user_content})
        console.print(Panel(config.additional_user_content, title="[green]Additional User Message[/green]", subtitle="Will be added before each of your requests"))

    if scan_result:
        messages.append({"role": "system", "content": f"Working on the project: {scan_result}."})
        console.print(Panel(f"Working on the project: {os.path.abspath(work_folder)}", title="[green]Project Path[/green]"))

    if initial_message:
        messages.append({"role": "user", "content": initial_message})
        console.print(Panel(initial_message, title="[green]Initial User Message[/green]"))

    return messages


def handle_user_interaction(messages: list) -> str:
    set_marker()
    role_user_content = prompt([('class:prompt', 'Query: ')], multiline=True, key_bindings=bindings, style=style)
    clear_to_marker()
    console.print(Panel(f"{role_user_content}", title="[green]User Query[/green]"))
    messages.append({"role": "user", "content": role_user_content})
    return role_user_content


def conversation(work_folder: str, need_scan: bool, structure_only: bool, initial_message: str = None) -> None:
    try:
        scan_result = scan_folder(work_folder, need_scan, structure_only)
        project_abspath = os.path.abspath(work_folder)
        messages = initialize_messages(scan_result, work_folder, initial_message)
        skip_user_question = bool(initial_message)
        # merged_functions = merge_functions_describes(work_folder)

        while True:
            num_tousend_tokens_from_messages(messages)

            if not skip_user_question:
                handle_user_interaction(messages)
            else:
                skip_user_question = False

            chat_response = chat_completion_request(messages, config.default_functions)
            token = chat_response.usage.total_tokens
            logger.info(f"Number of tokens counted by openai {token}, finish_reason: {chat_response.choices[0].finish_reason}")
            if chat_response.choices[0].finish_reason in ('length', 'tool_calls'):
                skip_user_question = True
            assistant_message = chat_response.choices[0].message
            messages.append(assistant_message)

            if assistant_message.content:
                console.print(Panel(Markdown(assistant_message.content), title="[green]GPT answer[/green]"))

            skip_user_question |= process_tool_calls(messages, assistant_message, project_abspath)
    except KeyboardInterrupt:
        logger.info("Finished")
    finally:
        logger.info("Session completed")
