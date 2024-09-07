import json
import logging
import os
import subprocess
from typing import Any

from morix.scan import get_project_structure
from morix.config_loader import load_yaml, config
from morix.helpers import read_file_content


logger = logging.getLogger(__name__)


def crud_files(arguments: Any, project_abspath: str):
    arguments = json.loads(arguments)
    result = []
    skip_question = False
    operations = {
        'create': ('created', 'w'),
        'read': ('read', None),
        'update': ('updated', 'w'),
        'delete': ('deleted', None)
    }

    for file in arguments['files']:
        filename = file['filename']
        file_path = os.path.join(project_abspath, filename)
        content = file.get('content', '')
        operation = file['operation']

        if operation in operations:
            action, mode = operations[operation]

            if operation == 'create':
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if operation == 'delete':
                if os.path.exists(file_path):
                    os.remove(file_path)
                else:
                    action = "does not exist"

            if mode:
                with open(file_path, mode, encoding='utf-8') as f:
                    f.write(content)

            if operation == 'read':
                content = read_file_content(file_path)
                result.append(f"{filename}: {content}")
                skip_question = True
            else:
                result.append(f"{filename}: {action}")

            logger.info(f"{filename}: {action}")
    result_str = "\n".join(result)
    return result_str, skip_question


def merge_functions(scan_folder: str):
    try:
        if os.path.exists(os.path.join(scan_folder, "functions.yml")):
            project_functions = load_yaml(scan_folder, "functions.yml")
            merged_functions = config.default_functions + project_functions
            return merged_functions
    except Exception as e:
        logger.error(f"Error loading functions from {project_functions}: {e}")

    return config.default_functions


def process_tool_calls(messages, assistant_message: dict, project_abspath: str):
    if not assistant_message.tool_calls:
        return False

    skip_user_question = False

    def handle_crud_files(tool):
        result, skip = crud_files(tool.function.arguments, project_abspath)
        messages.append({
            "tool_call_id": tool.id,
            "role": "tool",
            "name": 'save_files',
            "content": result,
        })
        return skip

    def handle_command(tool):
        if not config.permissions.get('allow_run_console_command', False):
            content = "Execution of console commands is not allowed based on the config settings."
            logger.warning(content)
        else:
            command = json.loads(tool.function.arguments)['command']
            timeout = json.loads(tool.function.arguments)['timeout']
            logging.info(f"Executing command '{command}' with timeout {timeout} seconds")
            try:
                process = subprocess.Popen(
                    ['sh', '-c', command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=project_abspath
                )

                output = ""
                for line in process.stdout:
                    print(line, end='')
                    output += line
                process.wait()

                logger.info(f"Command return code: {process.returncode}")

                if process.returncode != 0:
                    logger.error(f"Command failed with return code {process.returncode} and output: {output}")

                max_lines = config.command_output.get('max_output_lines', 100)
                stdout_lines = output.splitlines()[-max_lines:]
                trimmed_stdout = "\n".join(stdout_lines)
                content = trimmed_stdout or f"No command execution result received, exit code: {process.returncode}"
            except subprocess.TimeoutExpired:
                content = "The command was interrupted due to timeout expiration. One should seriously think about whether to increase the timeout or find a place to modify either the code or the tests."
                logger.error(content)

        messages.append({
            "tool_call_id": tool.id,
            "role": "tool",
            "name": 'command',
            "content": content,
        })
        return True

    def handle_read_directory_structure(tool):
        scan_folder = os.path.join(project_abspath, json.loads(tool.function.arguments)['project'])
        logging.info(f"Reading directory content {scan_folder}")
        scan_result = get_project_structure(scan_folder)
        messages.append({
            "tool_call_id": tool.id,
            "role": "tool",
            "name": 'run_test',
            "content": scan_result,
        })
        return True

    def handle_task_status(tool):
        status = json.loads(tool.function.arguments)['status']
        logging.info(f"Task status {status}")
        messages.append({
            "tool_call_id": tool.id,
            "role": "tool",
            "name": 'run_test',
            "content": "ok",
        })
        if status == 'Completed':
            return False
        return True

    handlers = {
        'crud_files': handle_crud_files,
        'run_console_command': handle_command,
        'task_status': handle_task_status,
        'read_directory_structure': handle_read_directory_structure
    }

    for tool in assistant_message.tool_calls:
        if tool.function.name in handlers:
            skip_user_question |= handlers[tool.function.name](tool)

    for tool in assistant_message.tool_calls:
        if tool.function.name == 'multi_tool_use':
            tool_uses = json.loads(tool.function.arguments)['tool_uses']
            for use in tool_uses:
                func_name = use['recipient_name'].replace("functions.", "")
                if func_name in handlers:
                    skip_user_question |= handlers[func_name](tool_uses)

    return skip_user_question

