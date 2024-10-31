import unittest
from socket import socket
from unittest.mock import patch, MagicMock
from requests.post import http_post, save_response_to_file
from response import Response

class TestHttpPostClient(unittest.TestCase):

    @patch('requests.post.socket.socket')
    def test_http_post_success(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        mock_sock_instance.recv.side_effect = [
            b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!",
            b''
        ]

        data = {'key': 'value'}
        response = http_post("http://example.com", data=data)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_content(), "Hello, world!")
        self.assertIn("Content-Length", response.headers)
        self.assertEqual(response.headers["Content-Length"], "13")

    @patch('requests.post.socket.socket')
    def test_http_post_with_headers_and_cookies(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        mock_sock_instance.recv.side_effect = [
            b"HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, world!",
            b''
        ]

        data = {'key': 'value'}
        headers = {'User-Agent': 'TestAgent'}
        cookies = {'session_id': '12345'}

        response = http_post("http://example.com", data=data, headers=headers, cookies=cookies)

        self.assertIsNotNone(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_content(), "Hello, world!")

    @patch('requests.post.socket.socket')
    def test_http_post_timeout(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_sock_instance.recv.side_effect = socket.timeout

        response = http_post("http://example.com")

        self.assertIsNone(response)

    @patch('requests.post.socket.socket')
    def test_http_post_connection_error(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_sock_instance.connect.side_effect = Exception("Connection error")
        response = http_post("http://example.com")

        self.assertIsNone(response)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_response_to_file(self, mock_open):
        response = Response("Hello, world!", 200, {"Content-Length": "13"})
        save_response_to_file(response, "testfile.txt")
        mock_open.assert_called_once_with("testfile.txt", 'w', encoding='utf-8')
        mock_open().write.assert_called_once_with("Hello, world!")

if __name__ == "__main__":
    unittest.main()
