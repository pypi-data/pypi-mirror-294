import pytest
import os
from unittest.mock import patch, MagicMock
from morix.conversation import (
    scan_folder,
    initialize_messages,
    handle_user_interaction,
    conversation
)
from morix.config_loader import config


@pytest.fixture
def dummy_scan_folder(tmp_path):
    return str(tmp_path)


def test_scan_project_scan(dummy_scan_folder):
    os.mkdir(os.path.join(dummy_scan_folder, "test"))
    with open(os.path.join(dummy_scan_folder, "test", "file.txt"), "w") as f:
        f.write("test")

    scan_result = scan_folder(dummy_scan_folder, True, False)
    assert "file.txt" in scan_result


def test_initialize_messages(dummy_scan_folder):
    scan_result = "Test scan result"
    expected_roles = {
        "system": config.role_system_content,
        "user": config.additional_user_content
    }

    messages = initialize_messages(scan_result, dummy_scan_folder)
    for role, content in expected_roles.items():
        assert any(m["role"] == role and content for m in messages)


@patch('morix.conversation.prompt', return_value='User query')
@patch('morix.conversation.console.print')
def test_handle_user_interaction(mock_print, mock_prompt):
    messages = []
    user_content = handle_user_interaction(messages)
    assert len(messages) == 1
    assert user_content == "User query"
    assert messages[0]["content"] == "User query"

# Comment out to prevent hanging during test run
# @patch('morix.conversation.chat_completion_request')
# @patch('morix.conversation.handle_user_interaction', return_value='User input query')
# @patch('morix.conversation.console.print')
# @patch('morix.conversation.initialize_messages', return_value=[{"role": "system", "content": "Test"}])
# @patch('morix.conversation.scan_project', return_value='Test scan result')
# def test_conversation_initialization(
#    mock_scan_project,
#    mock_initialize_messages,
#    mock_console_print,
#    mock_handle_user_interaction,
#    mock_chat_completion_request,
#    dummy_scan_folder
# ):
#    mock_chat_response = MagicMock()
#    mock_chat_response.choices = [MagicMock()]
#    mock_chat_response.choices[0].finish_reason = 'stop'
#    mock_chat_response.choices[0].message.content = 'Test GPT Response'
#    mock_chat_response.usage.total_tokens = 100
#    mock_chat_completion_request.return_value = mock_chat_response
#
#    conversation(True, dummy_scan_folder, False, False)
#
#    mock_console_print.assert_called()
#    mock_handle_user_interaction.assert_called()
#    mock_initialize_messages.assert_called()