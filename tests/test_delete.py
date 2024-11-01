import unittest
from unittest.mock import patch, MagicMock
from exceptions import TimeoutError, ConnectionError, RedirectError, ResponseDecodeError
from response import Response
from requests.get import http_get, save_response_to_file  # Импортируем функцию http_get
import socket


class TestHttpGet(unittest.TestCase):

    ...


if __name__ == "__main__":
    unittest.main()
