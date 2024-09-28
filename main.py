import typer
import requests
import json
import os

app = typer.Typer()


@app.command()
def get(url: str, params=None, save: bool = False):
    response = requests.get(url, params=params)
    if save:
        save_response(response)

@app.command()
def post(url: str, data=None, json_data=None, save: bool = False):
    response = requests.post(url, data=data, json=json_data)
    if save:
        save_response(response)

@app.command()
def put(url: str, data=None, json_data=None, save: bool = False):
    response = requests.put(url, data=data, json=json_data)
    if save:
        save_response(response)

@app.command()
def delete(url: str, save: bool = False):
    response = requests.delete(url)
    if save:
        save_response(response)


def count_files(directory):
    return len([file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))])


def save_response(response: requests.Response):
    dictionary = {
        'url': response.url,
        'request method': response.request.method,
        'timeout': str(response.elapsed),
        'headers': dict(response.headers),
        'body': str(response.url),
        'cookies': str(response.cookies),
    }

    if not os.path.exists('json'):
        os.makedirs('json')

    with open(f'json/saved_contents{count_files("json")}.json', 'w') as f:
        json.dump(dict(dictionary), f)


if __name__ == "__main__":
    app()
