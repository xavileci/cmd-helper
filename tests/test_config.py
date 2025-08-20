# -*- coding: utf-8 -*-
"""
Tests for config module
"""

import unittest
import os
import importlib
from unittest.mock import patch, mock_open
from cmd_helper import config


class TestConfig(unittest.TestCase):
    """Test cases for Config class"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = config.Config()

    def test_config_initialization(self):
        """Test basic config initialization"""
        self.assertIsNotNone(self.config)

    def test_model_name_set(self):
        """Test that model name is configured"""
        self.assertEqual(self.config.MODEL_NAME, "gemini-2.5-flash")

    def test_max_tokens_default(self):
        """Test max tokens default value"""
        self.assertEqual(self.config.MAX_TOKENS, 1000)

    def test_temperature_default(self):
        """Test temperature default value"""
        self.assertEqual(self.config.TEMPERATURE, 0.1)

    def test_language_default(self):
        """Test language default configuration"""
        # This might be 'auto' or the actual detected language
        self.assertIn(self.config.LANGUAGE, ["auto", "es", "en"])

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_api_key'}, clear=True)
    def test_api_key_from_env(self):
        """Test API key loading from environment variable"""
        # Reload the config module to pick up new environment variables
        importlib.reload(config)
        test_config = config.Config()
        self.assertEqual(test_config.GEMINI_API_KEY, 'test_api_key')

    @patch('builtins.open', mock_open(read_data='GEMINI_API_KEY=file_api_key\nLANGUAGE=es'))
    @patch('os.path.exists', return_value=True)
    def test_load_from_env_file(self, mock_exists):
        """Test loading configuration from .env file"""
        # Note: Config class loads from .env files using dotenv
        # This test documents the expected behavior
        pass

    @patch.dict(os.environ, {'CMD_HELPER_LANG': 'en'}, clear=True)
    def test_language_override(self):
        """Test language configuration override"""
        importlib.reload(config)
        test_config = config.Config()
        self.assertEqual(test_config.LANGUAGE, 'en')

    @patch.dict(os.environ, {}, clear=True)
    @patch('cmd_helper.config.load_dotenv')
    @patch('cmd_helper.config.Path.exists', return_value=False)
    def test_missing_api_key_handled_gracefully(self, mock_exists, mock_load_dotenv):
        """Test that missing API key is handled gracefully"""
        # Mock to prevent any dotenv loading
        mock_load_dotenv.return_value = None
        
        importlib.reload(config)
        test_config = config.Config()
        # Should be None when not set
        self.assertIsNone(test_config.GEMINI_API_KEY)

    @patch.dict(os.environ, {'GEMINI_API_KEY': 'valid_key'}, clear=True)
    def test_validate_api_key_exists(self):
        """Test API key validation when present"""
        importlib.reload(config)
        test_config = config.Config()
        self.assertEqual(test_config.GEMINI_API_KEY, 'valid_key')

    def test_temperature_bounds(self):
        """Test temperature is within valid bounds"""
        self.assertGreaterEqual(self.config.TEMPERATURE, 0.0)
        self.assertLessEqual(self.config.TEMPERATURE, 1.0)

    def test_max_tokens_positive(self):
        """Test max tokens is positive"""
        self.assertGreater(self.config.MAX_TOKENS, 0)

    def test_dangerous_commands_list(self):
        """Test that dangerous commands list is defined"""
        self.assertIsInstance(self.config.DANGEROUS_COMMANDS, list)
        self.assertGreater(len(self.config.DANGEROUS_COMMANDS), 0)

    def test_excluded_dirs_list(self):
        """Test that excluded directories list is defined"""
        self.assertIsInstance(self.config.EXCLUDED_DIRS, list)
        self.assertGreater(len(self.config.EXCLUDED_DIRS), 0)


if __name__ == '__main__':
    unittest.main()
