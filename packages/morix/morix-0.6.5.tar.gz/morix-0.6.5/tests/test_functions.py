import pytest
import os
import json
from unittest.mock import MagicMock, patch
from morix.functions import crud_files, merge_functions, process_tool_calls


# Подкорректируйте количество по умолчанию, чтобы тесты соответствовали теку...
updated_function_count = 4

default_function_count = 3  # Количество функций по умолчанию, используемых в тестах

@pytest.fixture
def dummy_project_path(tmp_path):
    # Создаем временную папку для тестов
    return str(tmp_path)

def test_crud_files_create(dummy_project_path):
    arguments = json.dumps({
        "files": [
            {"filename": "test.txt", "content": "Hello, World!", "operation": "create"}
        ]
    })

    result, skip_question = crud_files(arguments, dummy_project_path)

    filepath = os.path.join(dummy_project_path, "test.txt")

    assert os.path.isfile(filepath)
    with open(filepath, "r", encoding="utf-8") as file:
        assert file.read() == "Hello, World!"

    assert "test.txt: created" in result
    assert not skip_question

def test_crud_files_delete(dummy_project_path):
    filepath = os.path.join(dummy_project_path, "test.txt")

    with open(filepath, "w", encoding="utf-8") as file:
        file.write("Delete me")

    arguments = json.dumps({
        "files": [
            {"filename": "test.txt", "operation": "delete"}
        ]
    })

    result, skip_question = crud_files(arguments, dummy_project_path)

    assert not os.path.isfile(filepath)
    assert "test.txt: deleted" in result
    assert not skip_question

def test_crud_files_read_missing_file(dummy_project_path):
    arguments = json.dumps({
        "files": [
            {"filename": "missing.txt", "operation": "read"}
        ]
    })

    result, skip_question = crud_files(arguments, dummy_project_path)

    assert "missing.txt: " in result  # Ожидается пустое содержимое в результате
    assert skip_question

@patch("morix.functions.read_file_content", return_value="Mocked content")
def test_crud_files_invoke_read_function(mock_read, dummy_project_path):
    filepath = os.path.join(dummy_project_path, "read.txt")

    with open(filepath, "w", encoding="utf-8") as file:
        file.write("File content")

    arguments = json.dumps({
        "files": [
            {"filename": "read.txt", "operation": "read"}
        ]
    })

    result, skip_question = crud_files(arguments, dummy_project_path)

    print(f"Messages: {result}")

    # Проверяем, действительно ли был вызов функции read_file_content
    mock_read.assert_called_once_with(filepath)

def test_merge_functions_no_file(dummy_project_path):
    functions = merge_functions(dummy_project_path)
    assert len(functions) == updated_function_count

def test_merge_functions_with_file(dummy_project_path):
    functions_yml = os.path.join(dummy_project_path, 'functions.yml')
    with open(functions_yml, 'w', encoding='utf-8') as f:
        f.write('- type: function\n  function:\n    name: "dummy_function"\n')

    functions = merge_functions(dummy_project_path)

    # Проверяем, что в список функций добавлена новая функция сверху базовых функций
    assert len(functions) == updated_function_count + 1

@patch('morix.config_loader.Config')
def test_process_tool_calls_with_command(MockConfig, dummy_project_path):
    mock_config = MockConfig.return_value
    mock_config.permissions.allow_run_console_command = True
    messages = []
    tool_mock = MagicMock()
    tool_mock.function.name = 'run_console_command'
    tool_mock.function.arguments = json.dumps({'command': 'echo test', 'timeout': 5})
    tool_mock.id = 1

    assistant_message = MagicMock(tool_calls=[tool_mock])

    with patch('subprocess.Popen') as mock_popen:
        mock_proc = mock_popen.return_value
        mock_proc.stdout = iter(['test\n'])  # Add stdout attribute with iterable lines
        mock_proc.wait.return_value = None
        mock_proc.returncode = 0

        skip_user_question = process_tool_calls(messages, assistant_message, dummy_project_path)

    assert skip_user_question
    assert any("test" in m['content'] for m in messages)

def test_process_tool_calls_with_task_status(dummy_project_path):
    messages = []
    tool_mock = MagicMock()
    tool_mock.function.name = 'task_status'
    tool_mock.function.arguments = json.dumps({'status': 'Completed'})
    tool_mock.id = 1

    assistant_message = MagicMock(tool_calls=[tool_mock])

    skip_user_question = process_tool_calls(messages, assistant_message, dummy_project_path)

    print(f"Messages: {messages}")

    assert not skip_user_question
    assert any("ok" == m['content'] for m in messages)

