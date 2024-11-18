import unittest
from typer.testing import CliRunner
from main import app

runner = CliRunner()


class TestHttpClientCLI(unittest.TestCase):

    def test_get_cli(self):
        url = "https://jsonplaceholder.typicode.com/todos/1"
        headers = "Content-Type:application/json"
        result = runner.invoke(app, ["get", url, "--headers", headers, "--timeout", "500"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("200", result.output)

    def test_get_cli_ya_ru(self):
        url = "https://ya.ru"

        result = runner.invoke(app, ["get", url])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("200" in result.output or "301" in result.output or "302" in result.output)

if __name__ == '__main__':
    unittest.main()
