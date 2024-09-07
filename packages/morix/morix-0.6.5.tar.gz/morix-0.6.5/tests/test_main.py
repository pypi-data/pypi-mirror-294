import pytest
from unittest.mock import patch
import argparse
import logging
from morix.main import parse_args, handle_command, main



def test_parse_args_with_path():
    test_args = ["prog", "./data"]
    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.path == "./data"


def test_parse_args_with_contents_flag():
    test_args = ["prog", "--contents", "./data"]
    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.contents is True
        assert args.path == "./data"


def test_parse_args_with_structure_only_flag():
    test_args = ["prog", "--structure-only", "./data"]
    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.structure_only is True
        assert args.path == "./data"


def test_parse_args_with_config_flag():
    test_args = ["prog", "--config"]
    with patch("sys.argv", test_args):
        args = parse_args()
        assert args.config is True


@patch("morix.helpers.input", return_value="")  # Mock input to simulate pressing Enter
@patch("morix.main.open_config_file")
def test_handle_command_opens_config(mock_open_config_file, mock_input):
    args = argparse.Namespace(config=True, path="", contents=False, structure_only=False, message=None)
    handle_command(args)
    mock_open_config_file.assert_called_once()


@pytest.mark.parametrize("log_level", [logging.DEBUG, logging.INFO])
@patch("morix.helpers.input", return_value="")  # Mock input to simulate pressing Enter
@patch("morix.main.conversation")
def test_handle_command_runs_conversation_without_scan(mock_conversation, mock_input, log_level, caplog, tmp_path):
    caplog.set_level(log_level)

    data_dir = tmp_path / "data"
    data_dir.mkdir()
    args = argparse.Namespace(config=False, path=str(data_dir), contents=False, structure_only=False, message=None)

    # Patching logger before calling handle_command
    logger = logging.getLogger("morix.conversation")
    logger.setLevel(log_level)
    logger.addHandler(logging.StreamHandler())

    handle_command(args)
    mock_conversation.assert_called_once_with(str(data_dir), False, False, None)
    print(f"Captured logs with level {log_level}: {[message.message for message in caplog.records]}")
    assert any("Starting work on the project at:" in message.message for message in caplog.records)


@patch("morix.helpers.input", return_value="")  # Mock input to simulate pressing Enter
@patch("morix.main.conversation")
def test_handle_command_runs_conversation_with_content_scan(mock_conversation, mock_input, tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    args = argparse.Namespace(config=False, path=str(data_dir), contents=True, structure_only=False, message=None)
    handle_command(args)
    mock_conversation.assert_called_once_with(str(data_dir), True, False, None)


@patch("morix.helpers.input", return_value="")  # Mock input to simulate pressing Enter
@patch("morix.main.conversation")
def test_handle_command_runs_conversation_with_structure_scan(mock_conversation, mock_input, tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    args = argparse.Namespace(config=False, path=str(data_dir), contents=False, structure_only=True, message=None)
    handle_command(args)
    mock_conversation.assert_called_once_with(str(data_dir), True, True, None)


def test_main_calls_handle_command():
    with patch("morix.main.parse_args") as mock_parse_args, \
         patch("morix.main.handle_command") as mock_handle_command:
        mock_parse_args.return_value = argparse.Namespace(config=True, message=None)
        main()
        mock_handle_command.assert_called_once()

