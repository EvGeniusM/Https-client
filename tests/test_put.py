import unittest
from unittest.mock import patch, MagicMock
from socket import timeout as socket_timeout
from exceptions import ConnectionError, RedirectError
from urllib.parse import urlparse
from requests.put import (
    create_ssl_connection,
    build_put_request,
    get_response,
    handle_redirect,
    decode_response,
    extract_status_and_headers,
    extract_body,
    http_put
)


class TestHttpPutRequest(unittest.TestCase):

    '''@patch('ssl.create_default_context')
    @patch('socket.socket')
    def test_create_ssl_connection(self, mock_socket, mock_create_context):
        # Мокаем создание SSL-соединения
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_create_context.return_value = MagicMock()

        # Вызов тестируемой функции
        sock = create_ssl_connection('example.com', 1000)

        # Проверяем, что сокет был создан правильно
        mock_socket.assert_called_once_with(mock_socket.AF_INET, mock_socket.SOCK_STREAM)
        mock_create_context.return_value.wrap_socket.assert_called_once_with(mock_sock_instance, server_hostname='example.com')
        self.assertEqual(sock, mock_sock_instance)

    def test_build_put_request(self):
        url = 'https://example.com'
        data = 'key=value'
        headers = {'User-Agent': 'test'}
        cookies = {'session': 'abc123'}

        request = build_put_request(url, data, headers, cookies)

        # Проверка, что запрос сформирован правильно
        self.assertIn("PUT / HTTP/1.1\r\n", request)
        self.assertIn("Host: example.com\r\n", request)
        self.assertIn("Content-Length: 10\r\n", request)
        self.assertIn("User-Agent: test\r\n", request)
        self.assertIn("Cookie: session=abc123\r\n", request)
        self.assertIn('key=value', request)'''

    '''@patch('socket.socket')
    def test_get_response(self, mock_socket):
        # Мокаем сокет для получения данных
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_sock_instance.recv.return_value = b'HTTP/1.1 200 OK\r\n\r\n{"message":"Success"}'

        response = get_response(mock_sock_instance)

        # Проверяем, что ответ получен корректно
        self.assertEqual(response, b'HTTP/1.1 200 OK\r\n\r\n{"message":"Success"}')'''

    def test_handle_redirect(self):
        url = 'https://example.com'
        response_lines = [
            'HTTP/1.1 301 Moved Permanently',
            'Location: https://new-location.com'
        ]
        new_url = handle_redirect(url, response_lines, 0, 5)
        self.assertEqual(new_url, 'https://new-location.com')

    def test_handle_redirect_max_redirects(self):
        url = 'https://example.com'
        response_lines = [
            'HTTP/1.1 301 Moved Permanently',
            'Location: https://new-location.com'
        ]
        with self.assertRaises(RedirectError):
            handle_redirect(url, response_lines, 6, 5)

    def test_decode_response(self):
        response = b'HTTP/1.1 200 OK\r\n\r\n{"message":"Success"}'
        decoded = decode_response(response)
        self.assertEqual(decoded, 'HTTP/1.1 200 OK\r\n\r\n{"message":"Success"}')

    def test_extract_status_and_headers(self):
        response_str = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"message":"Success"}'
        status_code, headers, lines = extract_status_and_headers(response_str)

        self.assertEqual(status_code, 200)
        self.assertEqual(headers['Content-Type'], 'application/json')

    def test_extract_body(self):
        response_str = 'HTTP/1.1 200 OK\r\n\r\n{"message":"Success"}'
        body = extract_body(response_str)
        self.assertEqual(body, '{"message":"Success"}')

    '''@patch('socket.socket')
    @patch('ssl.create_default_context')
    def test_http_put(self, mock_create_context, mock_socket):
        # Мокаем функции и сокет
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_create_context.return_value = MagicMock()

        mock_sock_instance.recv.return_value = b'HTTP/1.1 200 OK\r\n\r\n{"message":"Success"}'
        mock_sock_instance.sendall.return_value = None

        # Пример успешного запроса
        url = 'https://example.com'
        response = http_put(url, data='key=value')

        # Проверка, что был вызван правильный запрос и возвращён правильный статус
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"message":"Success"}')
        self.assertEqual(response.headers['Content-Type'], 'application/json')

    @patch('socket.socket')
    @patch('ssl.create_default_context')
    def test_http_put_redirect(self, mock_create_context, mock_socket):
        # Мокаем сокет для редиректа
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance
        mock_create_context.return_value = MagicMock()

        mock_sock_instance.recv.side_effect = [
            b'HTTP/1.1 301 Moved Permanently\r\nLocation: https://new-location.com\r\n\r\n',
            b'HTTP/1.1 200 OK\r\n\r\n{"message":"Success"}'
        ]
        mock_sock_instance.sendall.return_value = None

        # Пример PUT-запроса с редиректом
        url = 'https://example.com'
        response = http_put(url, data='key=value', max_redirects=5)

        # Проверка, что редирект был обработан, и ответ с новым URL
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"message":"Success"}')'''

if __name__ == '__main__':
    unittest.main()
