#!/usr/bin/env python3
"""Unit tests for client module"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


#!/usr/bin/env python3
"""Unit tests for client module"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns expected payload"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected_payload)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns correct URL"""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/google/repos")


    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos method returns expected repo list"""
        expected_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = expected_payload

        with patch("client.GithubOrgClient._public_repos_url", new="mocked_url") as mock_repos_url:
            client = GithubOrgClient("google")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("mocked_url")
            mock_repos_url.assert_called_once()


from parameterized import parameterized
import unittest
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct bool based on license key."""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)



#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for GithubOrgClient.public_repos method."""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get with fixture side_effect."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url.endswith('/orgs/google'):
                return MockResponse(cls.org_payload)
            elif url.endswith('/orgs/google/repos'):
                return MockResponse(cls.repos_payload)
            return None

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos list."""
        client = GithubOrgClient('google')
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filtering repos with license key 'apache-2.0'."""
        client = GithubOrgClient('google')
        apache_repos = client.public_repos(license_key='apache-2.0')
        self.assertEqual(apache_repos, self.apache2_repos)


class MockResponse:
    """Mock response to emulate requests.Response with json method."""

    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data



def test_public_repos(self):
    """Integration test for public_repos"""
    self.assertEqual(self.client.public_repos(), self.expected_repos)

def test_public_repos_with_license(self):
    """Integration test for public_repos filtering by license"""
    self.assertEqual(self.client.public_repos(license="apache-2.0"), self.apache2_repos)

