import unittest

from http_libs.custom_requests import CustomResponse
from unittest.mock import patch, MagicMock


class TestInternetModule(unittest.TestCase):
    def setUp(self) -> None:
        self.path = r'http://storage-monitor.ru'
        # self.cr = CustomResponse(self.path)

    # def test_status(self):
    #     self.assertEqual(self.cr.get_response_status(), 200)

    @patch('custom_requests.requests')
    def test_status_mock(self, mock_requests):
        mock_requests.get.return_value = MagicMock(status_code=200)
        cr = CustomResponse(self.path)
        self.assertEqual(cr.get_response_status(), 200)


def launch_test_request():
    unittest.main(r"tests\test_request")


if __name__ == "__main__":
    launch_test_request()
