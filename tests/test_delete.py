import unittest
from unittest.mock import patch
from exceptions import (
    TimeoutError,
    ConnectionError,
    RedirectError,
    ResponseDecodeError
)
from requests.delete import (
    create_request,
    parse_response,
    handle_redirect,
    http_delete
)
from response import Response


class TestHTTPDeleteMethods(unittest.TestCase):

    def test_create_request(self):
        request = create_request('https://example.com/path?query=123', {'Header': 'Value'}, {'cookie': 'value'})
        expected_request = b"DELETE /path?query=123 HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\nHeader: Value\r\nCookie: cookie=value\r\n\r\n"
        self.assertEqual(request, expected_request)

    def test_parse_response(self):
        response = parse_response(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!")
        self.assertEqual(response.contents, "Hello, World!")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers, {"Content-Type": "text/plain"})
        with self.assertRaises(ResponseDecodeError):
            parse_response(b"")
        with self.assertRaises(ResponseDecodeError):
            parse_response(b"")


    def test_handle_redirect(self):
        url, redirect_count = handle_redirect('https://example.com', {'Location': '/new-path'}, 5, 0)
        self.assertEqual(url, 'https://example.com/new-path')
        self.assertEqual(redirect_count, 1)

        url, redirect_count = handle_redirect('https://example.com', {}, 5, 0)
        self.assertEqual(url, 'https://example.com')
        self.assertEqual(redirect_count, 0)

        with self.assertRaises(RedirectError):
            handle_redirect('https://example.com', {'Location': '/new-path'}, 1, 1)

    @patch('requests.delete.send_request')
    @patch('requests.delete.parse_response')
    @patch('requests.delete.handle_redirect')
    def test_http_delete_success(self, mock_handle_redirect, mock_parse_response, mock_send_request):
        mock_send_request.return_value = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!"
        mock_parse_response.return_value = Response("Hello, World!", 200, {"Content-Type": "text/plain"})
        mock_handle_redirect.return_value = ('https://example.com', 1)

        response = http_delete('https://example.com', headers={'Header': 'Value'}, cookies={'cookie': 'value'})
        self.assertEqual(response.contents, "Hello, World!")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers, {"Content-Type": "text/plain"})

    @patch('requests.delete.send_request')
    @patch('requests.delete.parse_response')
    @patch('requests.delete.handle_redirect')
    def test_http_delete_redirect(self, mock_handle_redirect, mock_parse_response, mock_send_request):
        mock_send_request.side_effect = [
            b"HTTP/1.1 302 Found\r\nLocation: /new-path\r\n\r\n",
            b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, World!"
        ]
        mock_parse_response.side_effect = [
            Response("", 302, {"Location": "/new-path"}),
            Response("Hello, World!", 200, {"Content-Type": "text/plain"})
        ]
        mock_handle_redirect.side_effect = [
            ('https://example.com/new-path', 1),
            ('https://example.com/new-path', 1)
        ]

        response = http_delete('https://example.com', headers={'Header': 'Value'}, cookies={'cookie': 'value'})
        self.assertEqual(response.contents, "Hello, World!")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers, {"Content-Type": "text/plain"})

    @patch('requests.delete.send_request')
    @patch('requests.delete.parse_response')
    @patch('requests.delete.handle_redirect')
    def test_http_delete_max_redirects(self, mock_handle_redirect, mock_parse_response, mock_send_request):
        mock_send_request.return_value = b"HTTP/1.1 302 Found\r\nLocation: /new-path\r\n\r\n"
        mock_parse_response.return_value = Response("", 302, {"Location": "/new-path"})
        mock_handle_redirect.return_value = ('https://example.com/new-path', 1)

        with self.assertRaises(RedirectError):
            http_delete('https://example.com', headers={'Header': 'Value'}, cookies={'cookie': 'value'}, max_redirects=0)

    @patch('requests.delete.send_request')
    @patch('requests.delete.parse_response')
    @patch('requests.delete.handle_redirect')
    def test_http_delete_timeout(self, mock_handle_redirect, mock_parse_response, mock_send_request):
        mock_send_request.side_effect = TimeoutError()

        with self.assertRaises(TimeoutError):
            http_delete('https://example.com', headers={'Header': 'Value'}, cookies={'cookie': 'value'})

    @patch('requests.delete.send_request')
    @patch('requests.delete.parse_response')
    @patch('requests.delete.handle_redirect')
    def test_http_delete_connection_error(self, mock_handle_redirect, mock_parse_response, mock_send_request):
        mock_send_request.side_effect = ConnectionError("An error occurred: Test exception")

        with self.assertRaises(ConnectionError):
            http_delete('https://example.com', headers={'Header': 'Value'}, cookies={'cookie': 'value'})


if __name__ == '__main__':
    unittest.main()