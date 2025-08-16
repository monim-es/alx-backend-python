#!/usr/bin/env python3
"""
Test file for client.py
"""
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for GithubOrgClient
    """
    
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, expected_payload, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once.
        """
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
