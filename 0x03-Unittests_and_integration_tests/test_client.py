#!/usr/bin/env python3
"""Parameterize and patch as decorators
"""

from typing import Mapping
from client import GithubOrgClient
import utils
import unittest
from parameterized import parameterized, param, parameterized_class
from unittest.mock import patch, PropertyMock
import fixtures


class TestGithubOrgClient(unittest.TestCase):
    """test GithubOrgClient
    """
    @parameterized.expand([
        param(org_name='google',
              expected="https://api.github.com/orgs/google"),
        param(org_name='abc',
              expected="https://api.github.com/orgs/abc")
    ])
    @patch('client.get_json')
    def test_org(self, mock_get_json, org_name, expected):
        """test GithubOrgClient.org returns the correct value
        """
        GithubOrgClient(org_name).org
        mock_get_json.assert_called_once_with(expected)

    def test_public_repos_url(self):
        """mock GithubOrgClient.org property
        """
        with patch.object(
                GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": 'https://api.github.com/orgs/google/repos'
            }
            resp = GithubOrgClient('google').org["repos_url"]
            self.assertEqual(resp, 'https://api.github.com/orgs/google/repos')

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns correct value and
           get_json and _public_repos_url called once.
        """
        mock_get_json.return_value = [
            {'id': 1, 'name': 'truth'},
            {'id': 2, 'name': 'ruby-openid-apps-discovery'},
            {'id': 3, 'name': 'autoparse'}
        ]
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = 'http://github.com/org/google'
            clnt = GithubOrgClient('google')
            expected = ['truth', 'ruby-openid-apps-discovery', 'autoparse']
            self.assertEqual(clnt.public_repos(), expected)
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        param(repo={"license": {"key": "my_license"}},
              license_key="my_license", expected=True),
        param(repo={"license": {"key": "other_license"}},
              license_key="my_license", expected=False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test if has_license returns correct output
        """
        has_key = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(has_key, expected)


def mocked_requests_get(*args, **kwargs):
    """mock requests with different url
    """
    class MockResponse:
        """Mock response
        """
        def __init__(self, json_data):
            self.json_data = json_data

        def json(self):
            """Function for returning json
            """
            return self.json_data

    if args[0] == 'https://api.github.com/orgs/google':
        return MockResponse(fixtures.TEST_PAYLOAD[0][0])
    if args[0] == fixtures.TEST_PAYLOAD[0][0]["repos_url"]:
        return MockResponse(fixtures.TEST_PAYLOAD[0][1])


@parameterized_class(
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
    [(fixtures.TEST_PAYLOAD[0][0],
      fixtures.TEST_PAYLOAD[0][1],
      fixtures.TEST_PAYLOAD[0][2],
      fixtures.TEST_PAYLOAD[0][3])]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration Test. mock http request
    """
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch(
            'requests.get', side_effect=mocked_requests_get
        )
        cls.get_patcher.start()
        cls.clnt = GithubOrgClient('google')

    @classmethod
    def tearDownClass(cls):
        """stop patcher
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """ test public repos with out licence
        """
        self.assertEqual(self.clnt.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """ test public_repos with licence
        """
        self.assertEqual(self.clnt.public_repos(license="apache-2.0"),
                         self.apache2_repos)
