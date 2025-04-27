from config.config_parser import YamlParser
from unittest.mock import patch, mock_open


def test_config():
    with patch("config.config.open", mock_open(read_data="TEST: config_test")):
        config = YamlParser("") 
        expected = "config_test"
        assert config.get("TEST") == expected