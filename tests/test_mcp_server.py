# -*- coding: utf-8 -*-
"""
Tests for mcp_server module
"""

import unittest
from unittest.mock import patch, MagicMock
from cmd_helper.mcp_server import MCPServer


class TestMCPServer(unittest.TestCase):
    """Test cases for MCPServer class"""

    def setUp(self):
        """Set up test fixtures"""
        with patch('cmd_helper.mcp_server.genai.configure'):
            with patch('cmd_helper.mcp_server.genai.GenerativeModel'):
                self.server = MCPServer()

    def test_parse_response_structured_format(self):
        """Test parsing structured response format"""
        response_text = """COMANDO: ls -la
EXPLICACIÓN: Lista archivos con detalles
PELIGRO: NO"""
        
        result = self.server._parse_response(response_text)
        
        self.assertEqual(result['command'], 'ls -la')
        self.assertEqual(result['explanation'], 'Lista archivos con detalles')
        self.assertFalse(result['is_dangerous'])

    def test_parse_response_english_format(self):
        """Test parsing English structured response format"""
        response_text = """COMMAND: find . -name "*.py"
EXPLANATION: Find Python files in current directory
DANGER: NO"""
        
        result = self.server._parse_response(response_text)
        
        self.assertEqual(result['command'], 'find . -name "*.py"')
        self.assertEqual(result['explanation'], 'Find Python files in current directory')
        self.assertFalse(result['is_dangerous'])

    def test_parse_response_dangerous_command(self):
        """Test parsing dangerous command response"""
        response_text = """COMANDO: rm -rf /
EXPLICACIÓN: Elimina todos los archivos del sistema
PELIGRO: SI"""
        
        result = self.server._parse_response(response_text)
        
        self.assertEqual(result['command'], 'rm -rf /')
        self.assertTrue(result['is_dangerous'])

    def test_parse_response_fallback_extraction(self):
        """Test fallback command extraction when no structured format"""
        response_text = """Aquí tienes el comando que necesitas:
        
ls -la | grep python
        
Este comando lista archivos y filtra por python"""
        
        result = self.server._parse_response(response_text)
        
        self.assertIsNotNone(result['command'])
        self.assertIn('ls', result['command'])

    def test_parse_response_empty_response(self):
        """Test parsing empty response"""
        response_text = ""
        
        result = self.server._parse_response(response_text)
        
        self.assertIsNone(result['command'])
        self.assertIsNotNone(result['explanation'])
        self.assertFalse(result['is_dangerous'])

    def test_parse_response_exception_handling(self):
        """Test exception handling in response parsing"""
        # Force an exception by passing None
        result = self.server._parse_response(None)
        
        self.assertIsNone(result['command'])
        self.assertIn('error', result['explanation'].lower())
        self.assertFalse(result['is_dangerous'])

    def test_extract_structured_data(self):
        """Test structured data extraction"""
        lines = [
            "COMANDO: pwd",
            "EXPLICACIÓN: Muestra directorio actual", 
            "PELIGRO: NO"
        ]
        
        result = self.server._extract_structured_data(lines)
        
        self.assertEqual(result['command'], 'pwd')
        self.assertEqual(result['explanation'], 'Muestra directorio actual')
        self.assertFalse(result['is_dangerous'])

    def test_process_command_line(self):
        """Test command line processing"""
        result = {'command': None, 'explanation': '', 'is_dangerous': False}
        
        self.server._process_command_line("COMANDO: echo hello", result)
        self.assertEqual(result['command'], 'echo hello')
        
        self.server._process_command_line("COMMAND: ls -l", result)
        self.assertEqual(result['command'], 'ls -l')

    def test_process_explanation_line(self):
        """Test explanation line processing"""
        result = {'command': None, 'explanation': '', 'is_dangerous': False}
        
        self.server._process_explanation_line("EXPLICACIÓN: Test explanation", result)
        self.assertEqual(result['explanation'], 'Test explanation')
        
        self.server._process_explanation_line("EXPLANATION: English explanation", result)
        self.assertEqual(result['explanation'], 'English explanation')

    def test_process_danger_line(self):
        """Test danger line processing"""
        result = {'command': None, 'explanation': '', 'is_dangerous': False}
        
        self.server._process_danger_line("PELIGRO: SI", result)
        self.assertTrue(result['is_dangerous'])
        
        result['is_dangerous'] = False
        self.server._process_danger_line("DANGER: YES", result)
        self.assertTrue(result['is_dangerous'])
        
        result['is_dangerous'] = False
        self.server._process_danger_line("PELIGRO: NO", result)
        self.assertFalse(result['is_dangerous'])

    def test_is_dangerous_response(self):
        """Test dangerous response detection"""
        self.assertTrue(self.server._is_dangerous_response("YES"))
        self.assertTrue(self.server._is_dangerous_response("SI"))
        self.assertTrue(self.server._is_dangerous_response("yes"))
        self.assertTrue(self.server._is_dangerous_response("si"))
        self.assertFalse(self.server._is_dangerous_response("NO"))
        self.assertFalse(self.server._is_dangerous_response("no"))

    def test_extract_fallback_command(self):
        """Test fallback command extraction"""
        lines = [
            "# This is a comment",
            "",
            "ls -la",
            "more content"
        ]
        
        result = self.server._extract_fallback_command(lines)
        self.assertEqual(result, "ls -la")

    def test_extract_fallback_command_no_valid_command(self):
        """Test fallback extraction with no valid command"""
        lines = [
            "# Only comments",
            "",
            "# Another comment"
        ]
        
        result = self.server._extract_fallback_command(lines)
        self.assertIsNone(result)

    @patch('cmd_helper.mcp_server.genai.GenerativeModel')
    def test_generate_command_success(self, mock_model_class):
        """Test successful command generation"""
        # Mock the model and response
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.text = "COMANDO: ls\nEXPLICACIÓN: Lista archivos\nPELIGRO: NO"
        mock_response.candidates = [MagicMock()]
        mock_model.generate_content.return_value = mock_response
        
        with patch('cmd_helper.mcp_server.genai.configure'):
            server = MCPServer()
            result = server.generate_command("listar archivos")
        
        self.assertEqual(result['command'], 'ls')
        self.assertFalse(result['is_dangerous'])

    @patch('cmd_helper.mcp_server.genai.GenerativeModel')
    def test_generate_command_safety_filter(self, mock_model_class):
        """Test command generation with safety filter block"""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        mock_response = MagicMock()
        mock_response.candidates = []  # Empty candidates = blocked by safety filter
        mock_model.generate_content.return_value = mock_response
        
        with patch('cmd_helper.mcp_server.genai.configure'):
            server = MCPServer()
            result = server.generate_command("comando peligroso")
        
        self.assertIsNone(result['command'])
        # Check for safety/security in both English and Spanish
        explanation_lower = result['explanation'].lower()
        self.assertTrue('safety' in explanation_lower or 'seguridad' in explanation_lower)

    @patch('cmd_helper.mcp_server.genai.GenerativeModel')
    def test_generate_command_finish_reason_safety(self, mock_model_class):
        """Test command generation with safety finish reason"""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        
        mock_candidate = MagicMock()
        mock_candidate.finish_reason = 2  # SAFETY
        
        mock_response = MagicMock()
        mock_response.candidates = [mock_candidate]
        mock_model.generate_content.return_value = mock_response
        
        with patch('cmd_helper.mcp_server.genai.configure'):
            server = MCPServer()
            result = server.generate_command("comando peligroso")
        
        self.assertIsNone(result['command'])

    @patch('cmd_helper.mcp_server.genai.GenerativeModel')
    def test_generate_command_exception(self, mock_model_class):
        """Test command generation with exception"""
        mock_model = MagicMock()
        mock_model_class.return_value = mock_model
        mock_model.generate_content.side_effect = Exception("API Error")
        
        with patch('cmd_helper.mcp_server.genai.configure'):
            server = MCPServer()
            result = server.generate_command("test command")
        
        self.assertIsNone(result['command'])
        self.assertIn('error', result['explanation'].lower())


if __name__ == '__main__':
    unittest.main()
