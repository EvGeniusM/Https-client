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


def create_socket(host, timeout):
    try:
        return socket.create_connection((host, 443), timeout=timeout)
    except socket.timeout:
        raise TimeoutError()
    except Exception as e:
        raise ConnectionError(f"Connection error: {e}")

def wrap_socket(sock, host):
    context = ssl.create_default_context()
    return context.wrap_socket(sock, server_hostname=host)


def build_request(path, host, headers=None, cookies=None):
    request_lines = [
        f"GET {path} HTTP/1.1\r\n",
        f"Host: {host}\r\n",
        "Connection: close\r\n"
    ]
    if headers:
        for key, value in headers.items():
            request_lines.append(f"{key}: {value}\r\n")
    if cookies:
        cookie_header = "; ".join(f"{key}={value}" for key, value in cookies.items())
        request_lines.append(f"Cookie: {cookie_header}\r\n")
    request_lines.append("\r\n")
    return ''.join(request_lines)


def send_request(wrapped_sock, request):
    wrapped_sock.sendall(request.encode())


def receive_response(wrapped_sock):
    response = b""
    while True:
        part = wrapped_sock.recv(4096)
        if not part:
            break
        response += part
    return response


def parse_response(response_str):
    response_lines = response_str.splitlines()
    if not response_lines:
        raise ResponseDecodeError("Empty response lines.")
    status_line = response_lines[0]
    try:
        status_code = int(status_line.split()[1])
    except (IndexError, ValueError):
        raise ResponseDecodeError(f"Invalid status line: {status_line}")
    return status_code, response_lines


def handle_redirects(status_code, response_lines, current_url):
    if status_code in (301, 302, 303, 307, 308):
        redirect_headers = {}
        for line in response_lines[1:]:
            if line == '':
                break
            try:
                key, value = line.split(': ', 1)
                redirect_headers[key] = value
            except ValueError:
                continue
        if 'Location' in redirect_headers:
            new_url = redirect_headers['Location']
            if not new_url.startswith('http'):
                new_url = urljoin(current_url, new_url)
            return new_url
    return None


def parse_headers(response_lines):
    headers = {}
    for line in response_lines[1:]:
        if line == '':
            break
        try:
            key, value = line.split(': ', 1)
            headers[key] = value
        except ValueError:
            continue
    return headers


def parse_content(response_str):
    if "\r\n\r\n" in response_str:
        return response_str.split("\r\n\r\n", 1)[1]
    return ""


def http_get(url, headers=None, cookies=None, timeout=1000, max_redirects=5):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'
    if parsed_url.query:
        path += '?' + parsed_url.query

    redirect_count = 0
    while redirect_count < max_redirects:
        sock = create_socket(host, timeout)
        with wrap_socket(sock, host) as wrapped_sock:
            request = build_request(path, host, headers, cookies)
            send_request(wrapped_sock, request)
            response = receive_response(wrapped_sock)
            if not response:
                raise ConnectionError("Received an empty response from the server.")
            try:
                response_str = response.decode("utf-8", errors="replace")
            except UnicodeDecodeError:
                raise ResponseDecodeError("Failed to decode response")
            status_code, response_lines = parse_response(response_str)
            new_url = handle_redirects(status_code, response_lines, url)
            if new_url:
                url = new_url
                parsed_url = urlparse(url)
                host = parsed_url.netloc
                path = parsed_url.path if parsed_url.path else '/'
                if parsed_url.query:
                    path += '?' + parsed_url.query
                redirect_count += 1
                continue
        break

    if redirect_count >= max_redirects:
        raise RedirectError()

    response_headers = parse_headers(response_lines)
    content = parse_content(response_str)
    return Response(content, status_code, response_headers)


def save_response_to_file(response, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.get_content())