import socket
import ssl
from urllib.parse import urlparse, urljoin
from response import Response
from exceptions import (
    TimeoutError,
    ConnectionError,
    RedirectError,
    ResponseDecodeError
)

def http_delete(url, headers=None, cookies=None, timeout=1000, max_redirects=5):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'

    if parsed_url.query:
        path += '?' + parsed_url.query

    redirect_count = 0
    context = ssl.create_default_context()

    while redirect_count < max_redirects:
        try:
            with socket.create_connection((host, 443), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as wrapped_sock:
                    request = [
                        f"DELETE {path} HTTP/1.1\r\n",
                        f"Host: {host}\r\n",
                        "Connection: close\r\n"
                    ]

                    if headers:
                        for key, value in headers.items():
                            request.append(f"{key}: {value}\r\n")

                    if cookies:
                        cookie_header = "; ".join([f"{key}={value}" for key, value in cookies.items()])
                        request.append(f"Cookie: {cookie_header}\r\n")

                    request.append("\r\n")
                    request_data = ''.join(request)
                    wrapped_sock.sendall(request_data.encode())

                    response = b""
                    while True:
                        part = wrapped_sock.recv(4096)
                        if not part:
                            break
                        response += part

                    if not response:
                        return Response("", 204, {})

                    try:
                        response_str = response.decode('utf-8', errors='replace')
                    except UnicodeDecodeError:
                        raise ResponseDecodeError()

                    response_lines = response_str.splitlines()

                    if not response_lines:
                        raise ResponseDecodeError("Empty response lines.")

                    status_line = response_lines[0]
                    try:
                        status_code = int(status_line.split()[1])
                    except (IndexError, ValueError):
                        raise ResponseDecodeError(f"Invalid status line: {status_line}")

                    if status_code in (301, 302, 303, 307, 308):
                        response_headers = {}
                        for line in response_lines[1:]:
                            if line == '':
                                break
                            try:
                                key, value = line.split(': ', 1)
                                response_headers[key] = value
                            except ValueError:
                                continue

                        if 'Location' in response_headers:
                            new_url = response_headers['Location']
                            if not new_url.startswith('http'):
                                new_url = urljoin(url, new_url)
                            url = new_url
                            parsed_url = urlparse(url)
                            host = parsed_url.netloc
                            path = parsed_url.path if parsed_url.path else '/'
                            if parsed_url.query:
                                path += '?' + parsed_url.query
                            redirect_count += 1
                            continue

                    response_headers = {}
                    for line in response_lines[1:]:
                        if line == '':
                            break
                        if ': ' in line:
                            key, value = line.split(': ', 1)
                            response_headers[key] = value

                    content = response_str.split("\r\n\r\n", 1)[1] if "\r\n\r\n" in response_str else ""

                    return Response(content, status_code, response_headers)

        except socket.timeout:
            raise TimeoutError()
        except Exception as e:
            raise ConnectionError(f"An error occurred: {e}")

    raise RedirectError()
