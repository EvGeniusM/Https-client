import typer
import requests
import json
import os


DESCRIPTION = ('Usage: python main.py [request method] <url> [options...] [headers] [timeout]\n headers: '
               '"header;header..." \n\n get: HTTP Get --params \n post: HTTP Post --data \n put: HTTP Put --data \n '
               'delete HTTP Delete')

app = typer.Typer()


@app.command()
def help():
    print(DESCRIPTION)


@app.command()
def get(url: str, params=None, data=None, headers=None, cookies=None, save=False, timeout=1000):
    headers = headers.strip().split(';')
    proc_headers = param_str_to_dict(headers)
    proc_cookies = param_str_to_dict(cookies)
    response = requests.get(url, headers=proc_headers, cookies=proc_cookies, params=params, data=data, timeout=int(timeout))
    if save:  # ?
        save_response_as_html(response)
    print(response.status_code)


@app.command()
def post(url: str, data=None, headers=None, cookies=None, json_data=None, save=False, timeout=1000):
    proc_headers = param_str_to_dict(headers)
    proc_cookies = param_str_to_dict(cookies)
    response = requests.post(url, headers=proc_headers, cookies=proc_cookies, data=data, json=json_data, timeout=int(timeout))
    if save:
        save_response_as_html(response)


@app.command()
def put(url: str, data=None, headers=None, json_data=None, save=False, timeout=1000):
    proc_headers = param_str_to_dict(headers)
    response = requests.put(url, headers=proc_headers, data=data, json=json_data, timeout=int(timeout))
    if save:
        save_response_as_html(response)


@app.command()
def delete(url: str, headers=None, save=False, timeout=1000):
    proc_headers = param_str_to_dict(headers)
    response = requests.delete(url, headers=proc_headers, timeout=int(timeout))
    if save:
        save_response_as_html(response)


def count_files(directory):
    return len([file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))])


def save_response_as_json(response: requests.Response):
    dictionary = {
        'url': response.url,
        'request method': response.request.method,
        'timeout': str(response.elapsed),
        'headers': dict(response.headers),
    }

    if not os.path.exists('json'):
        os.makedirs('json')

    with open(f'json/saved_contents{count_files("json")}.json', 'w') as f:
        json.dump(dict(dictionary), f)


def save_response_as_html(response: requests.Response):
    if not os.path.exists('html'):
        os.makedirs('html')

    with open(f'html/saved_contents{count_files("html")}.html', 'w') as f:
        f.write(response.content.decode(errors='ignore', encoding='windows-1251'))


def param_str_to_dict(raw: str) -> dict:
    pairs = raw.strip().split(';')
    result = dict()
    try:
        for pair in pairs:
            args = pair.split(':')
            args = [arg.strip() for arg in args]
            result[args[0]] = args[1]
    except Exception:
        print("Wrong param instruction, check 'help' to get info")
    return result


if __name__ == "__main__":
    app()
