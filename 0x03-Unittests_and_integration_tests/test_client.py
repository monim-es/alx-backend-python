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
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value
        and that get_json is called once.
        """
        # Set up the mock's return value
        mock_get_json.return_value = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}

        # Instantiate the client and call the method
        client = GithubOrgClient(org_name)
        result = client.org

        # Assertions
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"})
