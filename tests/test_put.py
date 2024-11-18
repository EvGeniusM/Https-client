import unittest
from unittest.mock import patch, MagicMock
from requests.put import (
    build_put_request,
    get_response,
    handle_redirect,
    decode_response,
    extract_status_and_headers,
    extract_body,
    http_put
)

class TestHTTPFunctions(unittest.TestCase):

    def test_build_put_request(self):
        url = "https://example.com/path"
        data = "data"
        headers = {"Header1": "Value1"}
        cookies = {"Cookie1": "Value1"}

        expected_request = (
            "PUT /path HTTP/1.1\r\n"
            "Host: example.com\r\n"
            "Connection: close\r\n"
            "Content-Length: 4\r\n"
            "Header1: Value1\r\n"
            "Cookie: Cookie1=Value1\r\n"
            "\r\n"
            "data"
        )

        request = build_put_request(url, data, headers, cookies)
        self.assertEqual(request, expected_request)

    def test_get_response(self):
        mock_sock = MagicMock()
        mock_sock.recv.side_effect = [b"HTTP/1.1 200 OK\r\n", b"\r\n", b"data", b""]
        response = get_response(mock_sock)
        self.assertEqual(response, b"HTTP/1.1 200 OK\r\n\r\ndata")

    def test_handle_redirect(self):
        response_lines = [
            "HTTP/1.1 302 Found",
            "Location: https://example.com/new_path",
            "",
            "Some body"
        ]
        new_url = handle_redirect("https://example.com/path", response_lines, 0, 5)
        self.assertEqual(new_url, "https://example.com/new_path")

    def test_decode_response(self):
        response = b"HTTP/1.1 200 OK\r\n\r\ndata"
        response_str = decode_response(response)
        self.assertEqual(response_str, "HTTP/1.1 200 OK\r\n\r\ndata")

    def test_extract_status_and_headers(self):
        response_str = "HTTP/1.1 200 OK\r\nHeader1: Value1\r\nHeader2: Value2\r\n\r\nbody"
        status_code, response_headers, response_lines = extract_status_and_headers(response_str)
        self.assertEqual(status_code, 200)
        self.assertEqual(response_headers, {"Header1": "Value1", "Header2": "Value2"})
        self.assertEqual(response_lines, ["HTTP/1.1 200 OK", "Header1: Value1", "Header2: Value2", "", "body"])

    def test_extract_body(self):
        response_str = "HTTP/1.1 200 OK\r\n\r\ndata"
        body = extract_body(response_str)
        self.assertEqual(body, "data")

    @patch('requests.put.create_ssl_connection')
    @patch('requests.put.build_put_request')
    @patch('requests.put.get_response')
    @patch('requests.put.decode_response')
    @patch('requests.put.extract_status_and_headers')
    @patch('requests.put.extract_body')
    def test_http_put(self, mock_extract_body, mock_extract_status_and_headers, mock_decode_response, mock_get_response, mock_build_put_request, mock_create_ssl_connection):
        mock_sock = MagicMock()
        mock_create_ssl_connection.return_value = mock_sock
        mock_get_response.return_value = b"HTTP/1.1 200 OK\r\n\r\ndata"
        mock_decode_response.return_value = "HTTP/1.1 200 OK\r\n\r\ndata"
        mock_extract_status_and_headers.return_value = (200, {}, ["HTTP/1.1 200 OK", "", "data"])
        mock_extract_body.return_value = "data"

        response = http_put("https://example.com/path", data="data")

        self.assertEqual(response.contents, "data")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers, {})

if __name__ == '__main__':
    unittest.main()