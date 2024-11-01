import typer
import os

from exceptions import InvalidParamError
from requests.get import http_get
from requests.post import http_post
from requests.put import http_put
from requests.delete import http_delete

DESCRIPTION = ('Usage: python main.py [request method] <url> [options...] [headers] [timeout]\n headers: '
               '"header;header..." \n\n get: HTTP Get --params \n post: HTTP Post --data \n put: HTTP Put --data \n '
               'delete HTTP Delete')

app = typer.Typer()


@app.command()
def help():
    print(DESCRIPTION)


@app.command()
def get(url: str, headers=None, cookies=None, save: bool = False, timeout=1000):
    if headers is not None:
        headers = param_str_to_dict(headers.strip())
    else:
        headers = {}
    if cookies is not None:
        cookies = param_str_to_dict(cookies.strip())
    else:
        cookies = {}
    response = http_get(url, cookies, headers, int(timeout))
    if save:
        save_response_as_html(response)
    print(response.status_code)
    return response


@app.command()
def post(url: str, data=None, headers=None, cookies=None, save: bool = False, timeout=1000):
    if headers is not None:
        headers = param_str_to_dict(headers)
    else:
        headers = {}
    if cookies is not None:
        cookies = param_str_to_dict(cookies)
    else:
        cookies = {}
    response = http_post(url, data, headers, cookies, int(timeout))
    if save:
        save_response_as_html(response)
    print(response.status_code)
    return response


@app.command()
def put(url: str, data=None, headers=None, cookies=None, save: bool = False, timeout=1000):
    if headers is not None:
        headers = param_str_to_dict(headers)
    else:
        headers = {}
    if cookies is not None:
        cookies = param_str_to_dict(cookies)
    else:
        cookies = {}
    response = http_put(url, data, headers, cookies, int(timeout))
    if save:
        save_response_as_html(response)
    print(response.status_code)
    return response


@app.command()
def delete(url: str, headers=None, cookies=None, save: bool = False, timeout=1000):
    if headers is not None:
        headers = param_str_to_dict(headers)
    else:
        headers = {}
    if cookies is not None:
        cookies = param_str_to_dict(cookies)
    else:
        cookies = {}
    response = http_delete(url, headers, cookies, int(timeout))
    if save:
        save_response_as_html(response)
    print(response.status_code)
    return response


def count_files(directory):
    return len([file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))])

def save_response_as_html(response):
    if not os.path.exists('html'):
        os.makedirs('html')

    filename = f'html/saved_contents{count_files("html")}.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(response.get_content())
    print(f"Сохранено в файл: {filename}")


def param_str_to_dict(raw: str) -> dict:
    if not raw.strip():  # Проверка на пустую строку или строку, состоящую из пробелов
        return {}

    pairs = raw.strip().split(';')
    result = {}
    for pair in pairs:
        # Разделяем по ':' или '=' в зависимости от наличия этих символов
        args = pair.split(':') if ':' in pair else pair.split('=')
        args = [arg.strip() for arg in args]  # Убираем лишние пробелы

        if len(args) == 2:  # Если есть ключ и значение
            result[args[0]] = args[1]
        else:
            raise InvalidParamError(f"Invalid pair format: {pair}")

    return result


if __name__ == "__main__":
    app()