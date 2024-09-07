import subprocess
import tempfile
import os
import logging
from venv import logger
from rich.panel import Panel
from rich.markdown import Markdown
from rich.console import Console
from prompt_toolkit import prompt
from colorama import init

from morix.functions import merge_functions, process_tool_calls

from .scan import scan, get_project_structure
from .helpers import clear_to_marker, get_string_size_kb, bindings, set_marker, style, num_tousend_tokens_from_messages
from .config_loader import role_system_content, additional_user_content
from .complection import chat_completion_request

# Initialize colorama for Windows
init()

console = Console()

logger = logging.getLogger(__name__)
# logger = logging.getLogger("morix.conversation")
# logger.setLevel(logging.DEBUG)  # Ensuring that debug messages are captured



def scan_folder(scan_folder: str, need_scan: bool, structure_only: bool) -> str:
    if not need_scan:
        return ""
    if structure_only:
        return get_project_structure(scan_folder)
    else:
        scan_result = scan(scan_folder)
        logger.debug(f"Scanning completed. Size in kilobytes: {get_string_size_kb(scan_result):.2f} KB.")
        return scan_result


def initialize_messages(scan_result: str, scan_folder: str) -> list:
    messages = []
    merge_functions(scan_folder)

    if role_system_content:
        messages.append({"role": "system", "content": role_system_content})
        console.print(Panel(role_system_content, title="[green]System Message[/green]"))

    if additional_user_content:
        messages.append({"role": "user", "content": additional_user_content})
        console.print(Panel(additional_user_content, title="[green]Additional User Message[/green]", subtitle="Will be added before each of your requests"))

    if scan_result:
        messages.append({"role": "system", "content": f"Working on the project: {scan_result}."})
        console.print(Panel(f"Working on the project: {os.path.abspath(scan_folder)}", title="[green]Project Path[/green]"))

    return messages


def handle_user_interaction(messages: list) -> str:
    set_marker()
    role_user_content = prompt([('class:prompt', 'Query: ')], multiline=True, key_bindings=bindings, style=style)
    clear_to_marker()
    console.print(Panel(f"{role_user_content}", title="[green]User Query[/green]"))
    messages.append({"role": "user", "content": role_user_content})
    return role_user_content


def conversation(workf_folder: str, need_scan: bool, structure_only: bool) -> None:
    try:
        scan_result = scan_folder(workf_folder, need_scan, structure_only)
        project_abspath = os.path.abspath(workf_folder)
        messages = initialize_messages(scan_result, workf_folder)
        skip_user_question = False
        merged_functions = merge_functions(workf_folder)

        while True:
            num_tousend_tokens_from_messages(messages)

            if not skip_user_question:
                handle_user_interaction(messages)
            else:
                skip_user_question = False

            chat_response = chat_completion_request(messages, merged_functions)
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
