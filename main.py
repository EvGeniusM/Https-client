import typer
import requests
import json
from os import path, makedirs

app = typer.Typer()


@app.command()
def get(url: str, save=False):
    request = requests.get(url)
    if save:
        dictionary = {
            'url': request.url,
            'request method': 'get',
            'timeout': str(request.elapsed),
            'headers': dict(request.headers),
        }

        if not path.exists('json'):
            makedirs('json')

        with open('json/saved_contents.json', 'w') as f:
            json.dump(dict(dictionary), f)
            print(save)
    else:
        print("I did nothing")


if __name__ == "__main__":
    app()
