import pytest
import requests
from typer.testing import CliRunner
from unittest.mock import patch, mock_open
from main import app, save_response, count_files

runner = CliRunner()


def test_get_request():
    url = "https://learn.microsoft.com/ru-ru/dotnet/csharp/advanced-topics/interop/using-type-dynamic"
    result = runner.invoke(app, ["get", url])
    assert result.exit_code == 0


def test_post_request(requests_mock):
    url = "https://learn.microsoft.com/ru-ru/dotnet/csharp/advanced-topics/interop/using-type-dynamic"
    requests_mock.post(url, json={"key": "value"}, status_code=200)

    result = runner.invoke(app, ["post", url, "--json-data", '{"key": "value"}'])

    assert result.exit_code == 0


def test_put_request(requests_mock):
    url = "https://learn.microsoft.com/ru-ru/dotnet/csharp/advanced-topics/interop/using-type-dynamic"
    requests_mock.put(url, json={"key": "value"}, status_code=200)

    result = runner.invoke(app, ["put", url, "--json-data", '{"key": "value"}'])

    assert result.exit_code == 0
    assert "key" in result.output


def test_delete_request(requests_mock):
    url = "https://learn.microsoft.com/ru-ru/dotnet/csharp/advanced-topics/interop/using-type-dynamic"
    requests_mock.delete(url, status_code=204)

    result = runner.invoke(app, ["delete", url])

    assert result.exit_code == 0


@patch("os.listdir", return_value=["saved_contents0.json"])
@patch("os.path.isfile", return_value=True)
def test_count_files(mock_isfile, mock_listdir):
    assert count_files("json") == 1


@patch("builtins.open", new_callable=mock_open)
@patch("os.makedirs")
@patch("os.path.exists", return_value=False)
def test_save_response(mock_exists, mock_makedirs, mock_open, requests_mock):
    url = "https://learn.microsoft.com/ru-ru/dotnet/csharp/advanced-topics/interop/using-type-dynamic"
    requests_mock.get(url, json={"key": "value"}, status_code=200)
    response = requests.get(url)

    save_response(response)

    mock_makedirs.assert_called_once_with("json")
    mock_open.assert_called_once_with("json/saved_contents0.json", "w")

    handle = mock_open()
    handle.write.assert_called_once()