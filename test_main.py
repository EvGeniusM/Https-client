import unittest
from unittest.mock import patch, MagicMock
import requests

# Предположим, что ваш метод get находится в файле my_module.py
from main import get


class TestGetMethod(unittest.TestCase):

    @patch('main.requests.get')
    def test_get_success(self, mock_get):
        # Настраиваем mock-объект для успешного ответа
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = 'http://example.com'
        response = get(url)

        # Проверяем, что статус код правильный
        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once_with(url, headers=None, cookies={}, params=None, data=None, timeout=1000)

    @patch('main.requests.get')
    def test_get_with_headers(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = 'http://example.com'
        headers = 'Authorization: Token; Content-Type: application/json'
        response = get(url, headers=headers)

        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once_with(
            url,
            headers={'Authorization': 'Token', 'Content-Type': 'application/json'},
            cookies={},
            params=None,
            data=None,
            timeout=1000
        )

    @patch('main.requests.get')
    def test_get_with_cookies(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = 'http://example.com'
        cookies = 'session_id=abc123; user_id=42'
        response = get(url, cookies=cookies)

        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once_with(
            url,
            headers=None,
            cookies={'session_id': 'abc123', 'user_id': '42'},
            params=None,
            data=None,
            timeout=1000
        )

    @patch('main.requests.get')
    def test_get_timeout(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = 'http://example.com'
        response = get(url, timeout=500)

        self.assertEqual(response.status_code, 200)
        mock_get.assert_called_once_with(
            url,
            headers=None,
            cookies={},
            params=None,
            data=None,
            timeout=500
        )

    @patch('main.requests.get')
    def test_get_save_response(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Патчим save_response_as_html для проверки вызова
        with patch('main.save_response_as_html') as mock_save:
            url = 'http://example.com'
            response = get(url, save=True)

            self.assertEqual(response.status_code, 200)
            mock_save.assert_called_once_with(mock_response)


if __name__ == '__main__':
    unittest.main()