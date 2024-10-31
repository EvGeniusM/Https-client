import unittest
from response import Response

class TestResponse(unittest.TestCase):
    def setUp(self):
        self.content = "Sample content"
        self.status_code = 200
        self.headers = {
            "Content-Type": "text/plain",
            "Content-Length": "15"
        }
        self.response = Response(self.content, self.status_code, self.headers)

    def test_get_status_code(self):
        self.assertEqual(self.response.get_status_code(), self.status_code)

    def test_get_headers(self):
        self.assertEqual(self.response.get_headers(), self.headers)

    def test_get_content(self):
        self.assertEqual(self.response.get_content(), self.content)

    def test_headers(self):
        self.assertIn("Content-Type", self.response.get_headers())
        self.assertEqual(self.response.get_headers()["Content-Type"], "text/plain")

    def test_content_length(self):
        self.assertEqual(self.response.get_headers()["Content-Length"], "15")

if __name__ == '__main__':
    unittest.main()
