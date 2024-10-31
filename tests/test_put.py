import unittest
from unittest.mock import patch, MagicMock
import socket
from urllib.parse import urlencode

import main
from response import Response


class TestHttpPut(unittest.TestCase):

    @patch('socket.socket')
    def test_http_put_success(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        response_data = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: 13\r\n"
            "\r\n"
            "Response body"
        )
        mock_sock_instance.recv.side_effect = [response_data.encode(), b'']

        url = "http://testurl.com/path"
        data = {'key': 'value'}
        headers = {'Custom-Header': 'Value'}
        cookies = {'session': 'abc123'}

        encoded_data = urlencode(data)

        response = main.http_put(url, data, headers, cookies)

        mock_sock_instance.connect.assert_called_once_with(('testurl.com', 80))

        expected_request = (
            f"PUT /path HTTP/1.1\r\n"
            f"Host: testurl.com\r\n"
            "Connection: close\r\n"
            f"Content-Length: {len(encoded_data)}\r\n"
            "Custom-Header: Value\r\n"
            "Cookie: session=abc123\r\n"
            "\r\n"
            f"{encoded_data}"
        )
        mock_sock_instance.sendall.assert_called_once_with(expected_request.encode())

        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_content(), "Response body")
        self.assertEqual(response.headers, {'Content-Length': '13'})

    @patch('socket.socket')
    def test_http_put_timeout(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_sock_instance.connect.side_effect = socket.timeout

        response = main.http_put("http://testurl.com/path")

        self.assertIsNone(response)

    @patch('socket.socket')
    def test_http_put_exception(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_sock_instance.connect.side_effect = Exception("Connection error")

        response = main.http_put("http://testurl.com/path")

        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()