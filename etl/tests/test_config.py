import pytest
from unittest.mock import patch, mock_open
from src.config.config_parser import KeyNotInConfigError, YamlParser


def test_config():
    with patch(
        "src.config.config_parser.open", mock_open(read_data="TEST: config_test")
    ):
        config = YamlParser("")
        expected = "config_test"
        assert config.get("TEST") == expected


def test_config_key_not_found():
    with patch(
        "src.config.config_parser.open", mock_open(read_data="TEST: config_test")
    ):
        config = YamlParser("")
        with pytest.raises(KeyNotInConfigError):
            config.get("DummyKey")
