import socket
from urllib.parse import urlparse
from response import Response

def http_delete(url, headers=None, cookies=None, timeout=1000):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    request = []

    try:
        sock.connect((host, 80))
        request.append(f"DELETE {path} HTTP/1.1\r\n")
        request.append(f"Host: {host}\r\n")
        request.append("Connection: close\r\n")

        if headers:
            for key, value in headers.items():
                request.append(f"{key}: {value}\r\n")

        if cookies:
            cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])
            request.append(f"Cookie: {cookie_header}\r\n")

        request.append("\r\n")
        request = ''.join(request)

        sock.sendall(request.encode())

        response = b""
        while True:
            part = sock.recv(4096)
            if not part:
                break
            response += part

        if not response:
            print("Received empty response.")
            return None

    except socket.timeout:
        print("Request timed out.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        sock.close()

    response_str = response.decode()
    response_lines = response_str.splitlines()

    if not response_lines:
        print("No response lines found.")
        return None

    status_line = response_lines[0]
    status_code = int(status_line.split()[1])

    headers = {}
    for line in response_lines[1:]:
        if line == '':
            break
        key, value = line.split(': ', 1)
        headers[key] = value

    content = response_str.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in response_str else ""

    return Response(content, status_code, headers)