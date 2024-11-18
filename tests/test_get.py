import unittest
from unittest.mock import patch, MagicMock
from exceptions import ResponseDecodeError
from requests.get import (create_socket, wrap_socket, build_request, send_request, receive_response, parse_response,
                           handle_redirects, parse_headers, parse_content, http_get)

class TestHTTPMethods(unittest.TestCase):

    @patch('socket.create_connection')
    def test_create_socket_success(self, mock_create_connection):
        mock_socket = MagicMock()
        mock_create_connection.return_value = mock_socket
        result = create_socket('example.com', 1000)
        self.assertIsNotNone(result)

    @patch('ssl.SSLContext.wrap_socket')
    def test_wrap_socket_success(self, mock_wrap_socket):
        mock_wrap_socket.return_value = MagicMock()
        result = wrap_socket(MagicMock(), 'example.com')
        self.assertIsNotNone(result)

    def test_build_request_no_headers_cookies(self):
        result = build_request('/path', 'example.com')
        expected = "GET /path HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
        self.assertEqual(result, expected)

    def test_build_request_with_headers_cookies(self):
        headers = {'User-Agent': 'test'}
        cookies = {'session': '123'}
        result = build_request('/path', 'example.com', headers, cookies)
        expected = "GET /path HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\nUser-Agent: test\r\nCookie: session=123\r\n\r\n"
        self.assertEqual(result, expected)

    def test_send_request(self):
        mock_socket = MagicMock()
        test_request = "GET /path HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
        send_request(mock_socket, test_request)
        mock_socket.sendall.assert_called_once_with(test_request.encode())

    @patch('socket.socket.recv')
    def test_receive_response(self, mock_recv):
        mock_recv.side_effect = [b'HTTP/1.1 200 OK\r\n', b'\r\n', b'Hello, World!', b'']
        mock_socket = MagicMock()
        mock_socket.recv = mock_recv
        result = receive_response(mock_socket)
        expected = b'HTTP/1.1 200 OK\r\n\r\nHello, World!'
        self.assertEqual(result, expected)

    def test_parse_response_success(self):
        response_str = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!"
        status_code, response_lines = parse_response(response_str)
        self.assertEqual(status_code, 200)
        self.assertEqual(response_lines, ["HTTP/1.1 200 OK", "Content-Type: text/html", "", "Hello, World!"])

    def test_parse_response_invalid_status(self):
        response_str = "HTTP/1.1 Invalid Status\r\nContent-Type: text/html\r\n\r\nHello, World!"
        with self.assertRaises(ResponseDecodeError):
            parse_response(response_str)

    def test_handle_redirects_success(self):
        response_lines = ["HTTP/1.1 302 Found", "Location: https://new.example.com", ""]
        new_url = handle_redirects(302, response_lines, "http://example.com")
        self.assertEqual(new_url, "https://new.example.com")

    def test_handle_redirects_no_location(self):
        response_lines = ["HTTP/1.1 302 Found", ""]
        new_url = handle_redirects(302, response_lines, "http://example.com")
        self.assertIsNone(new_url)

    def test_parse_headers(self):
        response_lines = ["HTTP/1.1 200 OK", "Content-Type: text/html", "Set-Cookie: session=123", ""]
        headers = parse_headers(response_lines)
        self.assertEqual(headers, {"Content-Type": "text/html", "Set-Cookie": "session=123"})

    def test_parse_content(self):
        response_str = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!"
        content = parse_content(response_str)
        self.assertEqual(content, "Hello, World!")

    @patch('requests.get.create_socket')
    @patch('requests.get.wrap_socket')
    @patch('requests.get.build_request')
    @patch('requests.get.send_request')
    @patch('requests.get.receive_response')
    @patch('requests.get.parse_response')
    @patch('requests.get.handle_redirects')
    @patch('requests.get.parse_headers')
    @patch('requests.get.parse_content')
    def test_http_get_success(self, mock_parse_content, mock_parse_headers, mock_handle_redirects, mock_parse_response,
                              mock_receive_response, mock_send_request, mock_build_request, mock_wrap_socket,
                              mock_create_socket):
        mock_create_socket.return_value = MagicMock()
        mock_wrap_socket.return_value = MagicMock()
        mock_build_request.return_value = 'GET /path HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n'
        mock_send_request.return_value = None
        mock_receive_response.return_value = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!'
        mock_parse_response.return_value = (200, ["HTTP/1.1 200 OK", "Content-Type: text/html", "", "Hello, World!"])
        mock_handle_redirects.return_value = None
        mock_parse_headers.return_value = {"Content-Type": "text/html"}
        mock_parse_content.return_value = "Hello, World!"

        response = http_get("http://example.com/path")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers, {"Content-Type": "text/html"})
        self.assertEqual(response.get_content(), "Hello, World!")

if __name__ == '__main__':
    unittest.main()