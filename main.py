import typer
import requests

app = typer.Typer()


@app.command()
def hello(url: str):
    request = requests.get(url)
    print(request.status_code)
    print(request.headers)
    print(request.text)


@app.command()
def goodbye():
    print("bye")


if __name__ == "__main__":
    app()
