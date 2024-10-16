import unittest
from unittest.mock import patch, MagicMock
from main import *


class TestGetMethod(unittest.TestCase):

    @patch('main.requests.get')
    def test_get_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        url = 'http://example.com'
        response = get(url)

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

        with patch('main.save_response_as_html') as mock_save:
            url = 'http://example.com'
            response = get(url, save=True)

            self.assertEqual(response.status_code, 200)
            mock_save.assert_called_once_with(mock_response)


    @patch('main.requests.post')
    def test_post_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        url = 'http://example.com'
        data = {'key': 'value'}
        headers = 'Content-Type: application/json'
        response = post(url, data=data, headers=headers)

        self.assertEqual(response.status_code, 201)
        mock_post.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            cookies={},
            data=data,
            json=None,
            timeout=1000
        )


    @patch('main.requests.post')
    def test_post_with_cookies(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        url = 'http://example.com'
        data = {'key': 'value'}
        headers = 'Content-Type: application/json'
        cookies = 'session_id=abc123; user_id=42'
        response = post(url, data=data, headers=headers, cookies=cookies)

        self.assertEqual(response.status_code, 201)
        mock_post.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            cookies={'session_id': 'abc123', 'user_id': '42'},
            data=data,
            json=None,
            timeout=1000
        )


    @patch('main.requests.post')
    def test_post_with_saving(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        data = {'key': 'value'}
        headers = 'Content-Type: application/json'

        with patch('main.save_response_as_html') as mock_save:
            url = 'http://example.com'
            response = post(url, data=data, headers=headers, save=True)

            self.assertEqual(response.status_code, 200)
            mock_save.assert_called_once_with(mock_response)


    @patch('main.requests.put')
    def test_put_success(self, mock_put):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_put.return_value = mock_response

        url = 'http://example.com'
        data = {'key': 'value'}
        headers = 'Content-Type: application/json'
        response = put(url, data=data, headers=headers)

        self.assertEqual(response.status_code, 200)
        mock_put.assert_called_once_with(
            url,
            headers={'Content-Type': 'application/json'},
            data=data,
            json=None,
            timeout=1000
        )


    @patch('main.requests.delete')
    def test_delete_success(self, mock_delete):
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_delete.return_value = mock_response

        url = 'http://example.com'
        headers = 'Authorization: Token'
        response = delete(url, headers=headers)

        self.assertEqual(response.status_code, 204)
        mock_delete.assert_called_once_with(
            url,
            headers={'Authorization': 'Token'},
            timeout=1000
        )


    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_count_files(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'directory']
        mock_isfile.side_effect = lambda x: not x.endswith('directory')
        directory = 'some_directory'
        count = count_files(directory)
        self.assertEqual(count, 2)
        mock_listdir.assert_called_once_with(directory)


    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_save_response_as_html_creates_directory(self, mock_exists, mock_makedirs):
        mock_exists.return_value = False
        mock_response = MagicMock()
        mock_response.content = b'<html><body>Response content</body></html>'
        save_response_as_html(mock_response)
        mock_makedirs.assert_called_once_with('html')


    @patch('os.makedirs')
    @patch('os.path.exists')
    def test_save_response_as_html_directory_exists(self, mock_exists, mock_makedirs):
        mock_exists.return_value = True
        mock_response = MagicMock()
        mock_response.content = b'<html><body>Response content</body></html>'
        save_response_as_html(mock_response)
        mock_makedirs.assert_not_called()


if __name__ == '__main__':
    unittest.main()