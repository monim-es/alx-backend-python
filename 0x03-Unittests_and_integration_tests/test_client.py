#!/usr/bin/env python3
import unittest
from unittest.mock import patch, PropertyMock
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
        """GithubOrgClient.org returns the mocked payload and calls get_json once"""
        mock_get_json.return_value = {"org": org_name}

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, {"org": org_name})

    def test_public_repos_url(self):
        """_public_repos_url is derived from the (mocked) org payload"""
        expected = "https://api.github.com/orgs/test-org/repos"
        payload = {"repos_url": expected}

        # Patch the property correctly using patch.object + PropertyMock
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = payload
            client = GithubOrgClient("test-org")
            self.assertEqual(client._public_repos_url, expected)


if __name__ == "__main__":
    unittest.main()
