class Response:
    def __init__(self, contents, status_code, headers):
        self.contents = contents
        self.status_code = status_code
        self.headers = headers

    def get_status_code(self):
        return self.status_code

    def get_headers(self):
        return self.headers

    def get_content(self):
        return self.contents