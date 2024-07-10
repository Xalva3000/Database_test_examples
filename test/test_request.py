import unittest

import requests

from http_libs.custom_requests import CustomResponse
from unittest.mock import patch, MagicMock
from requests.structures import CaseInsensitiveDict


class TestInternetModule(unittest.TestCase):
    def setUp(self) -> None:
        self.storage = r'http://storage-monitor.ru'
        self.httpbin = r'http://httpbin.org/'
        self.proxy = {'http': 'localhost:8080'}

    def test_status_storage(self):
        cr = CustomResponse(self.storage)
        self.assertTrue(cr.response.ok)
        self.assertEqual(cr.get_response_status(), 200)


    def test_status_httpbin(self):
        cr = CustomResponse(self.httpbin)
        self.assertTrue(cr.response.ok)
        self.assertEqual(cr.response.url, self.httpbin)
        self.assertEqual(cr.get_response_status(), 200)
        self.assertEqual(type(cr.get_response_headers()), CaseInsensitiveDict)

    def test_auth(self):
        cr = CustomResponse(self.httpbin)
        auth_dct = cr.get_authentication('alex', '12345').json()
        self.assertEqual(auth_dct['user'], 'alex')
        self.assertTrue(auth_dct['authenticated'])

    def test_custom_headers(self):
        new_headers = {'name': 'alex'}
        response = requests.get(self.httpbin, headers=new_headers)
        self.assertEqual(response.request.headers['name'], 'alex')

    def test_params(self):
        params = {1: 1, 2: 2}
        new_headers = {'name': 'alex'}
        response = requests.post(self.httpbin + 'post', headers=new_headers, params=params)
        self.assertEqual(response.json()['args'], {'1': '1', '2': '2'})

    def test_data(self):
        new_headers = {'name': 'alex'}
        params = {1: 1, 2: 2}
        data = {"username": "superuser"}
        response = requests.post(
            self.httpbin + 'post',
            headers=new_headers,
            params=params,
            json=data
        )
        self.assertEqual(response.json()['data'], '{"username": "superuser"}')

    def test_proxy(self):
        response = requests.get("http://ya.ru", proxies=proxy)

    @patch('http_libs.custom_requests.requests')
    def test_status_mock(self, mock_requests):
        mock_requests.get.return_value = MagicMock(status_code=200)
        cr = CustomResponse(self.storage)
        self.assertEqual(cr.response.status_code, 200)


def launch_test_request():
    unittest.main(r"tests\test_request")


if __name__ == "__main__":
    launch_test_request()


# python -m unittest test/test_request.py -v