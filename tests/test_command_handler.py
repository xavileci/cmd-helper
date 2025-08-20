# -*- coding: utf-8 -*-
"""
Tests for command_handler module
"""

import unittest
import subprocess
from unittest.mock import patch, MagicMock
from cmd_helper.command_handler import CommandHandler


class TestCommandHandler(unittest.TestCase):
    """Test cases for CommandHandler class"""

    def setUp(self):
        """Set up test fixtures"""
        self.handler = CommandHandler()

    def test_is_command_dangerous_rm_rf(self):
        """Test detection of dangerous rm -rf command"""
        dangerous_commands = [
            "rm -rf /",
            "sudo rm -rf /home",
            "rm -rf *",
            "sudo rm -rf /"
        ]
        
        for cmd in dangerous_commands:
            with self.subTest(command=cmd):
                self.assertTrue(self.handler.is_command_dangerous(cmd))

    def test_is_command_dangerous_dd(self):
        """Test detection of dangerous dd command"""
        dangerous_commands = [
            "dd if=/dev/zero of=/dev/sda",
            "sudo dd if=/dev/random of=/dev/disk0"
        ]
        
        for cmd in dangerous_commands:
            with self.subTest(command=cmd):
                self.assertTrue(self.handler.is_command_dangerous(cmd))

    def test_is_command_dangerous_safe_commands(self):
        """Test that safe commands are not flagged as dangerous"""
        safe_commands = [
            "ls -la",
            "cat file.txt",
            "mkdir new_directory",
            "cp file1.txt file2.txt",
            "find . -name '*.py'"
        ]
        
        for cmd in safe_commands:
            with self.subTest(command=cmd):
                self.assertFalse(self.handler.is_command_dangerous(cmd))

    def test_is_command_dangerous_chmod_777(self):
        """Test detection of dangerous chmod 777 command"""
        dangerous_commands = [
            "chmod 777 /",
            "sudo chmod -R 777 /usr"
        ]
        
        for cmd in dangerous_commands:
            with self.subTest(command=cmd):
                self.assertTrue(self.handler.is_command_dangerous(cmd))

    @patch('builtins.input', return_value='y')
    def test_confirm_execution_yes(self, mock_input):
        """Test command confirmation with yes response"""
        result = self.handler.confirm_execution("ls -la", "List files")
        self.assertTrue(result)

    @patch('builtins.input', return_value='n')
    def test_confirm_execution_no(self, mock_input):
        """Test command confirmation with no response"""
        result = self.handler.confirm_execution("ls -la", "List files")
        self.assertFalse(result)

    @patch('builtins.input', return_value='si')
    def test_confirm_execution_dangerous_yes_spanish(self, mock_input):
        """Test dangerous command confirmation with yes in Spanish"""
        result = self.handler.confirm_execution("rm -rf /tmp/test", "Delete files")
        self.assertTrue(result)

    @patch('builtins.input', return_value='no')
    def test_confirm_execution_dangerous_no(self, mock_input):
        """Test dangerous command confirmation with no response"""
        result = self.handler.confirm_execution("rm -rf /tmp/test", "Delete files")
        self.assertFalse(result)

    @patch('subprocess.run')
    def test_execute_command_success(self, mock_run):
        """Test successful command execution"""
        # Mock successful subprocess result
        mock_result = MagicMock()
        mock_result.stdout = "file1.txt\nfile2.txt"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = self.handler.execute_command("ls")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['stdout'], "file1.txt\nfile2.txt")
        self.assertEqual(result['return_code'], 0)
        self.assertTrue(result['success'])

    @patch('subprocess.run')
    def test_execute_command_with_error(self, mock_run):
        """Test command execution with error"""
        # Mock failed subprocess result
        mock_result = MagicMock()
        mock_result.stdout = ""
        mock_result.stderr = "Command not found"
        mock_result.returncode = 1
        mock_run.return_value = mock_result

        result = self.handler.execute_command("invalid_command")
        
        self.assertIsNotNone(result)
        self.assertEqual(result['stderr'], "Command not found")
        self.assertEqual(result['return_code'], 1)
        self.assertFalse(result['success'])

    @patch('subprocess.run')
    def test_execute_command_timeout(self, mock_run):
        """Test command execution timeout"""
        mock_run.side_effect = subprocess.TimeoutExpired(
            cmd="sleep 60", timeout=30
        )

        result = self.handler.execute_command("sleep 60")
        
        self.assertIsNotNone(result)
        self.assertIn('timeout', result.get('error', '').lower())

    @patch('subprocess.run')
    def test_execute_command_unicode_error_handling(self, mock_run):
        """Test command execution with unicode error handling"""
        # Mock subprocess result with encoding issues
        mock_result = MagicMock()
        mock_result.stdout = "Valid output with some � replaced chars"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        result = self.handler.execute_command("head /opt/binary_file")
        
        self.assertIsNotNone(result)
        self.assertIn("Valid output", result['stdout'])

        result = self.handler.execute_command("head /opt/binary_file")
        
        self.assertIsNotNone(result)
        self.assertIn("Valid output", result['stdout'])

    def test_dangerous_patterns_coverage(self):
        """Test coverage of dangerous command patterns"""
        patterns_to_test = [
            ("mkfs /dev/sda", True),
            ("dd if=/dev/zero of=/dev/sda", True), 
            ("rm -rf /", True),
            ("sudo rm -rf /tmp", True),
            ("chmod 777 /", True),
            ("echo 'safe'", False),
            ("curl -O file.txt", False),
            ("ls -la", False)
        ]
        
        for cmd, expected_dangerous in patterns_to_test:
            with self.subTest(command=cmd):
                result = self.handler.is_command_dangerous(cmd)
                self.assertEqual(result, expected_dangerous)


if __name__ == '__main__':
    unittest.main()
