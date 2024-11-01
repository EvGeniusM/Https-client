class HttpClientError(Exception):
    pass


class InvalidParamError(HttpClientError):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class TimeoutError(HttpClientError):
    def __init__(self, message="Request timed out"):
        super().__init__(message)
        self.message = message


class ConnectionError(HttpClientError):
    def __init__(self, message="Connection failed"):
        super().__init__(message)
        self.message = message


class RedirectError(HttpClientError):
    def __init__(self, message="Maximum redirect limit reached"):
        super().__init__(message)
        self.message = message


class ResponseDecodeError(HttpClientError):
    def __init__(self, message="Failed to decode response"):
        super().__init__(message)
        self.message = message
