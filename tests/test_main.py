# -*- coding: utf-8 -*-
"""
Tests for main module
"""

import unittest
import sys
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from cmd_helper.main import main, CmdHelper


class TestMain(unittest.TestCase):
    """Test cases for main module"""

    def setUp(self):
        """Set up test fixtures"""
        self.runner = CliRunner()

    def test_version_flag(self):
        """Test --version flag"""
        result = self.runner.invoke(main, ['--version'])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn('1.0.0', result.output)

    def test_help_flag(self):
        """Test --help flag"""
        result = self.runner.invoke(main, ['--help'])
        
        self.assertEqual(result.exit_code, 0)
        self.assertIn('Usage:', result.output)

    @patch('cmd_helper.main.CmdHelper')
    def test_main_with_request(self, mock_app_class):
        """Test main function with request argument"""
        mock_app = MagicMock()
        mock_app_class.return_value = mock_app
        
        result = self.runner.invoke(main, ['list files'])
        
        mock_app_class.assert_called_once()
        mock_app.process_request.assert_called_once_with('list files')

    def test_main_without_request_interactive(self):
        """Test main function without request (should show usage)"""
        result = self.runner.invoke(main, [])
        
        # Should show usage when no request provided
        self.assertEqual(result.exit_code, 0)
        # Accept both English and Spanish output
        self.assertTrue('Usage:' in result.output or 'Uso:' in result.output)

    @patch('cmd_helper.main.CmdHelper')
    def test_main_exception_handling(self, mock_app_class):
        """Test main function exception handling"""
        mock_app = MagicMock()
        mock_app.process_request.side_effect = Exception("Test error")
        mock_app_class.return_value = mock_app
        
        result = self.runner.invoke(main, ['test command'])
        
        # Should handle exception gracefully
        self.assertNotEqual(result.exit_code, 0)


class TestCmdHelper(unittest.TestCase):
    """Test cases for CmdHelper class"""

    def setUp(self):
        """Set up test fixtures"""
        with patch('cmd_helper.main.MCPServer'):
            with patch('cmd_helper.main.CommandHandler'):
                self.app = CmdHelper()

    @patch('cmd_helper.main.MCPServer')
    @patch('cmd_helper.main.CommandHandler')
    def test_app_initialization(self, mock_handler_class, mock_server_class):
        """Test CmdHelper initialization"""
        app = CmdHelper()
        
        mock_server_class.assert_called_once()
        mock_handler_class.assert_called_once()
        self.assertIsNotNone(app.mcp_server)
        self.assertIsNotNone(app.command_handler)

    def test_validate_setup_success(self):
        """Test successful setup validation"""
        self.app.config.GEMINI_API_KEY = "test_key"
        
        result = self.app.validate_setup()
        
        self.assertTrue(result)

    @patch('builtins.print')
    def test_validate_setup_failure(self, mock_print):
        """Test setup validation failure"""
        self.app.config.GEMINI_API_KEY = None
        
        result = self.app.validate_setup()
        
        self.assertFalse(result)
        mock_print.assert_called()

    @patch('builtins.print')
    def test_process_request_success(self, mock_print):
        """Test successful request processing"""
        # Mock successful response
        mock_result = {
            'command': 'ls -la',
            'explanation': 'List files',
            'is_dangerous': False
        }
        self.app.mcp_server.generate_command.return_value = mock_result
        
        # Mock user confirmation
        with patch.object(self.app.command_handler, 'confirm_execution', return_value=True):
            with patch.object(self.app.command_handler, 'execute_command') as mock_execute:
                mock_execute.return_value = {'success': True}
                
                self.app.process_request("list files")
                
                mock_execute.assert_called_once_with('ls -la')

    @patch('builtins.print')
    def test_process_request_no_command(self, mock_print):
        """Test request processing when no command is generated"""
        # Mock response with no command
        mock_result = {
            'command': None,
            'explanation': 'Could not generate command',
            'is_dangerous': False
        }
        self.app.mcp_server.generate_command.return_value = mock_result
        
        self.app.process_request("invalid request")
        
        # Should handle gracefully without trying to execute
        self.app.command_handler.execute_command.assert_not_called()

    @patch('builtins.print')
    def test_process_request_user_cancels(self, mock_print):
        """Test request processing when user cancels execution"""
        mock_result = {
            'command': 'ls -la',
            'explanation': 'List files',
            'is_dangerous': False
        }
        self.app.mcp_server.generate_command.return_value = mock_result
        
        # Mock user cancellation
        with patch.object(self.app.command_handler, 'confirm_execution', return_value=False):
            self.app.process_request("list files")
            
            # Should not execute command
            self.app.command_handler.execute_command.assert_not_called()

    @patch('builtins.print')
    def test_process_request_execution_failure(self, mock_print):
        """Test request processing with execution failure"""
        mock_result = {
            'command': 'invalid_command',
            'explanation': 'Test command',
            'is_dangerous': False
        }
        self.app.mcp_server.generate_command.return_value = mock_result
        
        # Mock user confirmation and failed execution
        with patch.object(self.app.command_handler, 'confirm_execution', return_value=True):
            with patch.object(self.app.command_handler, 'execute_command') as mock_execute:
                mock_execute.return_value = {'success': False}
                
                self.app.process_request("test request")
                
                mock_execute.assert_called_once_with('invalid_command')

    @patch('builtins.print')
    def test_process_request_exception_handling(self, mock_print):
        """Test request processing exception handling"""
        # Mock exception in mcp_server
        self.app.mcp_server.generate_command.side_effect = Exception("API Error")
        
        # Should handle exception gracefully
        try:
            self.app.process_request("test request")
        except Exception:
            self.fail("process_request should handle exceptions gracefully")


if __name__ == '__main__':
    unittest.main()
