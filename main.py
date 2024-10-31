import typer
import os
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
    # response = requests.get(url, headers=headers, cookies=cookies, params=params, data=data, timeout=int(timeout))
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
    # response = requests.post(url, headers=headers, cookies=cookies, data=data, json=json_data, timeout=int(timeout))
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

    with open(f'html/saved_contents{count_files("html")}.html', 'w') as f:
        f.write(response.content.decode(errors='ignore', encoding='windows-1251'))


def param_str_to_dict(raw: str) -> dict:
    pairs = raw.strip().split(';')
    result = {}
    try:
        for pair in pairs:
            args = pair.split(':') if ':' in pair else pair.split('=')
            args = [arg.strip() for arg in args]
            if len(args) == 2:
                result[args[0]] = args[1]
            else:
                print(f"Invalid pair format: {pair}")
    except Exception as e:
        print(f"Wrong param instruction, check 'help' to get info: {e}")
    return result


if __name__ == "__main__":
    app()
