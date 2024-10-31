import unittest
from unittest.mock import patch, MagicMock
import socket
from response import Response
import main


class TestHttpDelete(unittest.TestCase):

    @patch('socket.socket')
    def test_http_delete_success(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        response_data = (
            "HTTP/1.1 204 No Content\r\n"
            "Content-Length: 0\r\n"
            "\r\n"
        )
        mock_sock_instance.recv.side_effect = [response_data.encode(), b'']

        url = "http://testurl.com/path"
        headers = {'Custom-Header': 'Value'}
        cookies = {'session': 'abc123'}

        response = main.http_delete(url, headers, cookies)

        mock_sock_instance.connect.assert_called_once_with(('testurl.com', 80))

        expected_request = (
            "DELETE /path HTTP/1.1\r\n"
            "Host: testurl.com\r\n"
            "Connection: close\r\n"
            "Custom-Header: Value\r\n"
            "Cookie: session=abc123\r\n"
            "\r\n"
        )
        mock_sock_instance.sendall.assert_called_once_with(expected_request.encode())

        self.assertIsInstance(response, Response)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.get_content(), "")
        self.assertEqual(response.headers, {'Content-Length': '0'})

    @patch('socket.socket')
    def test_http_delete_timeout(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_sock_instance.connect.side_effect = socket.timeout

        response = main.http_delete("http://testurl.com/path")

        self.assertIsNone(response)

    @patch('socket.socket')
    def test_http_delete_exception(self, mock_socket):
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_sock_instance.connect.side_effect = Exception("Connection error")

        response = main.http_delete("http://testurl.com/path")

        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
