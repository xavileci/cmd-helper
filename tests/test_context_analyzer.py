# -*- coding: utf-8 -*-
"""
Tests for context_analyzer module
"""

import unittest
import os
import platform
from unittest.mock import patch, MagicMock
from cmd_helper.context_analyzer import ContextAnalyzer


class TestContextAnalyzer(unittest.TestCase):
    """Test cases for ContextAnalyzer class"""

    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = ContextAnalyzer()

    def test_get_current_context(self):
        """Test getting current system context"""
        context = self.analyzer.get_current_context()
        
        self.assertIsInstance(context, dict)
        self.assertIn('platform', context)
        self.assertIn('pwd', context)
        self.assertIn('env_vars', context)

    def test_context_has_required_fields(self):
        """Test that context contains all required fields"""
        context = self.analyzer.get_current_context()
        
        required_fields = ['platform', 'pwd', 'env_vars', 'files', 'git_info', 'recent_commands']
        for field in required_fields:
            with self.subTest(field=field):
                self.assertIn(field, context)
                self.assertIsNotNone(context[field])

    def test_platform_detection(self):
        """Test platform detection"""
        context = self.analyzer.get_current_context()
        
        self.assertIsInstance(context['platform'], dict)
        self.assertIn('system', context['platform'])
        self.assertIn('release', context['platform'])
        self.assertIn('shell', context['platform'])

    @patch('os.getcwd')
    def test_current_directory_detection(self, mock_getcwd):
        """Test current directory detection"""
        mock_getcwd.return_value = '/test/directory'
        
        context = self.analyzer.get_current_context()
        
        self.assertEqual(context['pwd'], '/test/directory')

    def test_user_detection(self):
        """Test user detection through environment"""
        context = self.analyzer.get_current_context()
        
        # User should be in env_vars
        self.assertIn('env_vars', context)
        # env_vars could be empty if USER is not set
        if 'USER' in context['env_vars']:
            self.assertIsInstance(context['env_vars']['USER'], str)

    def test_context_serializable(self):
        """Test that context is JSON serializable"""
        import json
        
        context = self.analyzer.get_current_context()
        
        try:
            json.dumps(context)
        except (TypeError, ValueError):
            self.fail("Context should be JSON serializable")

    @patch('platform.system')
    def test_platform_detection_variants(self, mock_system):
        """Test different platform detection scenarios"""
        platforms = ['Darwin', 'Linux', 'Windows']
        
        for platform_name in platforms:
            with self.subTest(platform=platform_name):
                mock_system.return_value = platform_name
                analyzer = ContextAnalyzer()
                context = analyzer.get_current_context()
                self.assertEqual(context['platform']['system'], platform_name)

    @patch('os.getcwd')
    def test_cwd_exception_handling(self, mock_getcwd):
        """Test current directory exception handling"""
        mock_getcwd.side_effect = OSError("Permission denied")
        
        # Should handle the exception gracefully - in this case it raises
        with self.assertRaises(OSError):
            self.analyzer.get_current_context()

    def test_context_consistency(self):
        """Test that context remains consistent across calls"""
        context1 = self.analyzer.get_current_context()
        context2 = self.analyzer.get_current_context()
        
        # Platform should be the same
        self.assertEqual(context1['platform'], context2['platform'])
        # pwd should be the same
        self.assertEqual(context1['pwd'], context2['pwd'])

    def test_context_data_types(self):
        """Test that context values have correct data types"""
        context = self.analyzer.get_current_context()
        
        self.assertIsInstance(context['platform'], dict)
        self.assertIsInstance(context['pwd'], str)
        self.assertIsInstance(context['env_vars'], dict)
        self.assertIsInstance(context['files'], list)
        self.assertIsInstance(context['git_info'], dict)

    def test_context_non_empty_values(self):
        """Test that context values are not empty"""
        context = self.analyzer.get_current_context()
        
        # These should always have values
        self.assertTrue(context['platform'], "Platform should not be empty")
        self.assertTrue(context['pwd'], "pwd should not be empty")
        
        # These can be empty but should be present
        self.assertIn('env_vars', context)
        self.assertIn('files', context)
        self.assertIn('git_info', context)
        self.assertIn('recent_commands', context)

    def test_git_info_structure(self):
        """Test git info structure"""
        context = self.analyzer.get_current_context()
        git_info = context['git_info']
        
        self.assertIn('is_git_repo', git_info)
        if git_info['is_git_repo']:
            self.assertIn('branch', git_info)
            self.assertIn('has_changes', git_info)

    def test_files_structure(self):
        """Test files list structure"""
        context = self.analyzer.get_current_context()
        files = context['files']
        
        self.assertIsInstance(files, list)
        # If there are files, check their structure
        if files and 'error' not in files[0]:
            for file_info in files[:3]:  # Check first 3 files
                self.assertIn('name', file_info)
                self.assertIn('type', file_info)
                self.assertIn(file_info['type'], ['file', 'dir'])


if __name__ == '__main__':
    unittest.main()
