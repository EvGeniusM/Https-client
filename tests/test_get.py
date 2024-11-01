import unittest
from unittest.mock import patch, MagicMock, mock_open  # Импортируем mock_open
from response import Response
from requests.get import http_get, save_response_to_file
import socket
import ssl


class TestHttpClient(unittest.TestCase):


    @patch('builtins.open', new_callable=mock_open)  # Теперь mock_open импортирован
    def test_save_response_to_file(self, mock_open):
        response = Response("Test content", 200, {"Content-Type": "text/plain"})
        save_response_to_file(response, "testfile.txt")

        mock_open.assert_called_once_with("testfile.txt", 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with("Test content")


if __name__ == "__main__":
    unittest.main()
