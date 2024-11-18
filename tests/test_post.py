import unittest
from unittest.mock import patch, MagicMock
from requests.post import (
    parse_url,
    build_request,
    send_request,
    parse_response,
    handle_redirects,
    http_post,
    Response,
    ConnectionError,
    RedirectError
)


class TestHttpClientFunctions(unittest.TestCase):

    def test_parse_url_with_full_path_and_query(self):
        url = "https://example.com/path?query=1"
        host, path = parse_url(url)
        self.assertEqual(host, "example.com")
        self.assertEqual(path, "/path")  # Путь без параметров запроса

    def test_build_request(self):
        request = build_request(
            host="example.com",
            path="/path",
            data="key=value",
            headers={"Header1": "Value1"},
            cookies={"cookie1": "value1"}
        )
        expected_request = (
            "POST /path HTTP/1.1\r\n"
            "Host: example.com\r\n"
            "Connection: close\r\n"
            "Content-Length: 9\r\n"
            "Header1: Value1\r\n"
            "Cookie: cookie1=value1\r\n"
            "\r\n"
            "key=value"
        )
        self.assertEqual(request, expected_request)

    @patch('requests.post.socket.create_connection')
    @patch('requests.post.ssl.create_default_context')
    def test_send_request(self, mock_ssl_context, mock_create_connection):
        mock_sock = MagicMock()
        mock_create_connection.return_value = mock_sock
        mock_ssl_context.return_value.wrap_socket.return_value = mock_sock

        mock_sock.recv.side_effect = [b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello, world!", b""]
        response = send_request("example.com", "POST /path HTTP/1.1\r\n", 1000)

        self.assertEqual(response, b"HTTP/1.1 200 OK\r\nContent-Length: 12\r\n\r\nHello, world!")

    def test_parse_response(self):
        response_bytes = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Type: text/html; charset=utf-8\r\n"
            b"Content-Length: 12\r\n"
            b"\r\n"
            b"Hello, world!"
        )
        response = parse_response(response_bytes)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.contents, "Hello, world!")
        self.assertEqual(response.headers, {
            "Content-Type": "text/html; charset=utf-8",
            "Content-Length": "12"
        })

    def test_handle_redirects(self):
        new_url, redirect_count = handle_redirects(
            url="https://example.com",
            headers={"Location": "https://new-example.com"},
            redirect_count=0,
            max_redirects=5
        )
        self.assertEqual(new_url, "https://new-example.com")
        self.assertEqual(redirect_count, 1)

        new_url, redirect_count = handle_redirects(
            url="https://example.com",
            headers={"Location": "/new-path"},
            redirect_count=0,
            max_redirects=5
        )
        self.assertEqual(new_url, "https://example.com/new-path")
        self.assertEqual(redirect_count, 1)

    @patch('requests.post.send_request')
    @patch('requests.post.parse_response')
    def test_http_post_success(self, mock_parse_response, mock_send_request):
        mock_send_request.return_value = (
            b"HTTP/1.1 200 OK\r\n"
            b"Content-Length: 12\r\n"
            b"\r\n"
            b"Hello, world!"
        )
        mock_parse_response.return_value = Response("Hello, world!", 200, {})

        response = http_post("https://example.com", data={"key": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.contents, "Hello, world!")

    @patch('requests.post.send_request')
    def test_http_post_connection_error(self, mock_send_request):
        mock_send_request.side_effect = Exception("Connection failed")
        with self.assertRaises(ConnectionError):
            http_post("https://example.com", data={"key": "value"})

    @patch('requests.post.send_request')
    @patch('requests.post.parse_response')
    def test_http_post_redirect(self, mock_parse_response, mock_send_request):
        mock_send_request.side_effect = [
            (
                b"HTTP/1.1 302 Found\r\n"
                b"Location: https://example.com/new-location\r\n"
                b"Content-Length: 0\r\n"
                b"\r\n"
            ),
            (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Length: 12\r\n"
                b"\r\n"
                b"Hello, world!"
            )
        ]
        mock_parse_response.side_effect = [
            Response("", 302, {"Location": "https://example.com/new-location"}),
            Response("Hello, world!", 200, {})
        ]

        response = http_post("https://example.com", data={"key": "value"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.contents, "Hello, world!")

    @patch('requests.post.send_request')
    @patch('requests.post.parse_response')
    def test_http_post_max_redirects(self, mock_parse_response, mock_send_request):
        mock_send_request.return_value = (
            b"HTTP/1.1 302 Found\r\n"
            b"Location: https://example.com/new-location\r\n"
            b"Content-Length: 0\r\n"
            b"\r\n"
        )
        mock_parse_response.return_value = Response("", 302, {"Location": "https://example.com/new-location"})

        with self.assertRaises(RedirectError):
            http_post("https://example.com", data={"key": "value"}, max_redirects=5)



if __name__ == '__main__':
    unittest.main()