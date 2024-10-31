import unittest
from socket import socket
from unittest.mock import patch, MagicMock, mock_open
from response import Response
from requests.get import http_get, save_response_to_file


class TestHttpClient(unittest.TestCase):

    @patch('requests.get.socket.socket')
    def test_http_get_success(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        mock_sock_instance.recv.side_effect = [
            b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!",
            b''
        ]

        response = http_get("http://example.com")

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_content(), "Hello, world!")
        self.assertIn("Content-Length", response.headers)
        self.assertEqual(response.headers["Content-Length"], "13")

    @patch('requests.get.socket.socket')
    def test_http_get_timeout(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        mock_sock_instance.connect.side_effect = socket.timeout

        response = http_get("http://example.com")
        self.assertIsNone(response)

    @patch('requests.get.socket.socket')
    def test_http_get_with_headers_and_cookies(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        mock_sock_instance.recv.side_effect = [
            b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!",
            b''
        ]

        headers = {'User-Agent': 'TestAgent'}
        cookies = {'session_id': '12345'}
        response = http_get("http://example.com", headers=headers, cookies=cookies)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_content(), "Hello, world!")
        self.assertIn("Content-Length", response.headers)
        self.assertEqual(response.headers["Content-Length"], "13")


    @patch('builtins.open', new_callable=mock_open)
    def test_save_response_to_file(self, mock_open):
        response = Response("Test content", 200, {"Content-Type": "text/plain"})
        save_response_to_file(response, "testfile.txt")

        mock_open.assert_called_once_with("testfile.txt", 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with("Test content")


if __name__ == "__main__":
    unittest.main()
