import pytest
from unittest.mock import patch, mock_open
from morix.config_loader import load_config


def test_load_config_missing_file():
    with patch('os.path.exists', return_value=False):
        with pytest.raises(FileNotFoundError):
            load_config()


@patch("builtins.open", new_callable=mock_open, read_data="gpt_model: test_model")
@patch("os.path.exists", return_value=True)
def test_load_config(mock_exists, mock_open):
    config = load_config()
    assert config["gpt_model"] == "test_model"
