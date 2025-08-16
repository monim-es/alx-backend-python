    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected repo names"""

        # Fake payload returned by get_json
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = test_payload

        # Patch _public_repos_url as context manager
        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_repos_url:

            mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            # Assert result is only repo names
            expected = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected)

            # Assert both mocks were called once
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test-org/repos")
