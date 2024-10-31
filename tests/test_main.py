import unittest
from unittest.mock import patch, MagicMock, mock_open
from response import Response
import main

class TestHttpClient(unittest.TestCase):

    @patch('main.http_get')
    def test_get(self, mock_http_get):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.content = b'Test response content'
        mock_http_get.return_value = mock_response

        response = main.get("http://testurl.com")
        self.assertEqual(response.status_code, 200)
        mock_http_get.assert_called_once_with("http://testurl.com", {}, {}, 1000)

    @patch('main.http_post')
    def test_post(self, mock_http_post):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 201
        mock_response.content = b'Test response content'
        mock_http_post.return_value = mock_response

        response = main.post("http://testurl.com", data='test_data')

        self.assertEqual(response.status_code, 201)
        mock_http_post.assert_called_once_with("http://testurl.com", 'test_data', {}, {}, 1000)

    @patch('main.http_put')
    def test_put(self, mock_http_put):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 204
        mock_http_put.return_value = mock_response

        response = main.put("http://testurl.com", data='test_data')

        self.assertEqual(response.status_code, 204)
        mock_http_put.assert_called_once_with("http://testurl.com", 'test_data', {}, {}, 1000)

    @patch('main.http_delete')
    def test_delete(self, mock_http_delete):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_http_delete.return_value = mock_response

        response = main.delete("http://testurl.com")

        self.assertEqual(response.status_code, 200)
        mock_http_delete.assert_called_once_with("http://testurl.com", {}, {}, 1000)

    @patch('main.save_response_as_html')
    @patch('main.http_get')
    def test_get_with_save(self, mock_http_get, mock_save_response_as_html):
        mock_response = MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.content = b'Test response content'
        mock_http_get.return_value = mock_response

        response = main.get("http://testurl.com", save=True)

        self.assertEqual(response.status_code, 200)
        mock_save_response_as_html.assert_called_once_with(mock_response)

    @patch('os.listdir')
    @patch('os.path.isfile')
    def test_count_files(self, mock_isfile, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt', 'directory1']
        mock_isfile.side_effect = lambda x: 'file' in x
        count = main.count_files('test_directory')
        self.assertEqual(count, 2)


    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists')
    @patch('main.count_files', return_value=0)
    def test_save_response_as_html(self, mock_count_files, mock_exists, mock_open_file, mock_makedirs):
        mock_exists.return_value = False
        mock_response = MagicMock()
        mock_response.content = b'Test content'
        main.save_response_as_html(mock_response)
        mock_makedirs.assert_called_once_with('html')
        mock_open_file.assert_called_once_with('html/saved_contents0.html', 'w')
        mock_open_file().write.assert_called_once_with('Test content')

    def test_param_str_to_dict(self):
        result = main.param_str_to_dict("key1:value1;key2:value2;key3=value3")
        expected = {
            'key1': 'value1',
            'key2': 'value2',
            'key3': 'value3'
        }
        self.assertEqual(result, expected)

        result_invalid = main.param_str_to_dict("key1:value1;invalid_pair")
        expected_invalid = {
            'key1': 'value1'
        }
        self.assertEqual(result_invalid, expected_invalid)

        result_empty = main.param_str_to_dict("")
        self.assertEqual(result_empty, {})

if __name__ == '__main__':
    unittest.main()