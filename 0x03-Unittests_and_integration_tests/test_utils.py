#!/usr/bin/env python3
"""unitest module
"""

from parameterized import parameterized, param
import unittest
import utils
from unittest.mock import patch
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """ unittest class
    """
    @parameterized.expand([
        param(nested_map={"a": 1}, path=("a",), expected=1),
        param(nested_map={"a": {"b": 2}}, path=("a",), expected={"b": 2}),
        param(nested_map={"a": {"b": 2}}, path=("a", "b"), expected=2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ test case for access_nested_map."""
        self.assertEqual(utils.access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        param(nested_map={}, path=("a",)),
        param(nested_map={"a": 1}, path=("a", "b"))
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """ test exception. """
        with self.assertRaises(KeyError):
            utils.access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """ Mocking HTTP request
    """
    @parameterized.expand([
        param(test_url="http://example.com", test_payload={"payload": True},
              expected={"payload": True}),
        param(test_url="http://holberton.io", test_payload={"payload": False},
              expected={"payload": False})
    ])
    def test_get_json(self, test_url, test_payload, expected):
        """mock requests.get
        """
        with patch('utils.requests.get') as mock_requ:
            mock_resp = unittest.mock.Mock()
            mock_resp.json.return_value = test_payload
            mock_requ.return_value = mock_resp
            self.assertEqual(utils.get_json(test_url), expected)
            mock_requ.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """ Test momorize
    """
    def test_memoize(self):
        """ Test memoize
        """
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock_method:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock_method.assert_called_once()
