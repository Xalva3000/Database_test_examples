import os
import unittest
import uuid

import requests
from requests import TooManyRedirects, ConnectTimeout

from http_libs.custom_requests import CustomResponse
from unittest.mock import patch, MagicMock
from requests.structures import CaseInsensitiveDict
from requests.cookies import RequestsCookieJar
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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

    # def test_proxy(self):
    #     response = requests.get("http://ya.ru", proxies=proxy)

    def test_cookies(self):
        # self.httpbin + 'cookies'
        cookies = {'i': uuid.uuid4()}
        cr = CustomResponse('http://ya.ru')
        self.assertEqual(type(cr.get_cookies()), RequestsCookieJar)
        self.assertEqual(type(cr.get_cookies().items()), list)

    def test_max_redirect(self):
        with self.assertRaises(TooManyRedirects) as e1:
            CustomResponse(self.httpbin + 'absolute-redirect/31')

    def test_redirect(self):
        cr = CustomResponse(self.httpbin + 'absolute-redirect/5')
        self.assertEqual(len(cr.response.history), 5)

    def test_timeout(self):
        with self.assertRaises(ConnectTimeout) as e1:
            requests.get(self.httpbin, timeout=0.1)


    def test_download(self):
        url = 'https://upload.wikimedia.org/wikipedia/ru/thumb/2/2d/%D0%9F%D1%80%D0%BE%D1%81%D1%82%D0%BE_%D1%82%D0%B0%D0%BA_-_%D0%BA%D0%B0%D0%B4%D1%80_%D0%B8%D0%B7_%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%B0.JPG/260px-%D0%9F%D1%80%D0%BE%D1%81%D1%82%D0%BE_%D1%82%D0%B0%D0%BA_-_%D0%BA%D0%B0%D0%B4%D1%80_%D0%B8%D0%B7_%D0%BC%D1%83%D0%BB%D1%8C%D1%82%D1%84%D0%B8%D0%BB%D1%8C%D0%BC%D0%B0.JPG'
        response = requests.get(url, verify=False, stream=True)
        with open('test/pic.jpg', 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        file_size = os.path.getsize('test/pic.jpg')
        self.assertTrue(file_size > 10)

    def test_upload(self):
        url = self.httpbin + 'anything'
        with open('test/pic.jpg', 'rb') as file:
            response = requests.post(url, data=file)
        self.assertTrue(response.ok)
        self.assertTrue(isinstance(response.__dict__['_content'], bytes))

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