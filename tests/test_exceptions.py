import unittest

from exceptions import InvalidParamError, TimeoutError, ConnectionError, RedirectError, ResponseDecodeError


class TestHttpClientErrors(unittest.TestCase):

    def test_invalid_param_error(self):
        message = "Invalid parameter"
        error = InvalidParamError(message)
        self.assertEqual(error.message, message)
        self.assertIsInstance(error, InvalidParamError)

    def test_timeout_error(self):
        error = TimeoutError()
        self.assertEqual(error.message, "Request timed out")
        self.assertIsInstance(error, TimeoutError)

    def test_timeout_error_with_custom_message(self):
        message = "Custom timeout message"
        error = TimeoutError(message)
        self.assertEqual(error.message, message)
        self.assertIsInstance(error, TimeoutError)

    def test_connection_error(self):
        error = ConnectionError()
        self.assertEqual(error.message, "Connection failed")
        self.assertIsInstance(error, ConnectionError)

    def test_connection_error_with_custom_message(self):
        message = "Custom connection error message"
        error = ConnectionError(message)
        self.assertEqual(error.message, message)
        self.assertIsInstance(error, ConnectionError)

    def test_redirect_error(self):
        error = RedirectError()
        self.assertEqual(error.message, "Maximum redirect limit reached")
        self.assertIsInstance(error, RedirectError)

    def test_redirect_error_with_custom_message(self):
        message = "Custom redirect error message"
        error = RedirectError(message)
        self.assertEqual(error.message, message)
        self.assertIsInstance(error, RedirectError)

    def test_response_decode_error(self):
        error = ResponseDecodeError()
        self.assertEqual(error.message, "Failed to decode response")
        self.assertIsInstance(error, ResponseDecodeError)

    def test_response_decode_error_with_custom_message(self):
        message = "Custom decode error message"
        error = ResponseDecodeError(message)
        self.assertEqual(error.message, message)
        self.assertIsInstance(error, ResponseDecodeError)


if __name__ == "__main__":
    unittest.main()
