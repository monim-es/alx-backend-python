#!/usr/bin/env python3
"""
Test file for client.py
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from utils import get_json

class TestGithubOrgClient(unittest.TestCase):
    """
    Test cases for GithubOrgClient
    """
    
    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once.
        """
        mock_payload = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, mock_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

if __name__ == '__main__':
    unittest.main()
