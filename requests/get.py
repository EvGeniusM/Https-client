import socket
from urllib.parse import urlparse
from response import Response


def http_get(url, headers=None, cookies=None, timeout=1000):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'

    if parsed_url.query:
        path += '?' + parsed_url.query
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    request = []

    try:
        sock.connect((host, 80))
        request.append(f"GET {path} HTTP/1.1\r\n")
        request.append(f"Host: {host}\r\n")
        request.append("Connection: close\r\n")

        if headers:
            for key, value in headers.items():
                request.append(f"{key}: {value}\r\n")

        if cookies:
            for key, value in cookies.items():
                request.append(f"Set-Cookie: {key}={value}")

        request.append("\r\n")
        request = ''.join(request)

        sock.sendall(request.encode())

        response = b""
        while True:
            part = sock.recv(4096)
            if not part:
                break
            response += part

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


def save_response_to_file(response, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.get_content())
