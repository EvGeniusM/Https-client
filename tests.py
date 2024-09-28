import pytest
import requests
import requests_mock
import os
import json
from typer.testing import CliRunner
from main import app

runner = CliRunner()


# Фикстура для очистки директории с json перед тестами
@pytest.fixture(autouse=True)
def clean_json_folder():
    if os.path.exists('json'):
        for f in os.listdir('json'):
            os.remove(os.path.join('json', f))
    yield
    if os.path.exists('json'):
        for f in os.listdir('json'):
            os.remove(os.path.join('json', f))


def test_get_request(requests_mock):
    url = "https://ya.ru"
    requests_mock.get(url, text='mocked response')

    result = runner.invoke(app, ['get', url, '--save'])
    assert result.exit_code == 0

    # Проверяем, что файл был создан
    assert os.path.exists('json/saved_contents0.json')

    # Проверяем содержимое файла
    with open('json/saved_contents0.json', 'r') as f:
        saved_data = json.load(f)
        assert saved_data['url'] == url + '/'
        assert saved_data['request method'] == 'GET'





def test_post_request(requests_mock):
    url = "https://ya.ru"
    requests_mock.post(url, text='mocked response')

    result = runner.invoke(app, ['post', url, '--save'])
    assert result.exit_code == 0

    # Проверяем, что файл был создан
    assert os.path.exists('json/saved_contents0.json')

    # Проверяем содержимое файла
    with open('json/saved_contents0.json', 'r') as f:
        saved_data = json.load(f)
        assert saved_data['url'] == url + '/'
        assert saved_data['request method'] == 'POST'


def test_put_request(requests_mock):
    url = "https://ya.ru"
    requests_mock.put(url, text='mocked response')

    result = runner.invoke(app, ['put', url, '--save'])
    assert result.exit_code == 0

    # Проверяем, что файл был создан
    assert os.path.exists('json/saved_contents0.json')

    # Проверяем содержимое файла
    with open('json/saved_contents0.json', 'r') as f:
        saved_data = json.load(f)
        assert saved_data['url'] == url + '/'
        assert saved_data['request method'] == 'PUT'


def test_delete_request(requests_mock):
    url = "https://ya.ru"
    requests_mock.delete(url, text='mocked response')

    result = runner.invoke(app, ['delete', url, '--save'])
    assert result.exit_code == 0

    # Проверяем, что файл был создан
    assert os.path.exists('json/saved_contents0.json')

    # Проверяем содержимое файла
    with open('json/saved_contents0.json', 'r') as f:
        saved_data = json.load(f)
        assert saved_data['url'] == url + '/'
        assert saved_data['request method'] == 'DELETE'