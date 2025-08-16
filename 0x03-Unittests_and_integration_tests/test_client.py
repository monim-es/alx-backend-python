#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Arrange: mock return value
        mock_get_json.return_value = {"org": org_name}

        # Act: create client and access org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert: get_json called once with the right URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"org": org_name})


if __name__ == "__main__":
    unittest.main()
