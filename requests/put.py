import socket
import ssl
from urllib.parse import urlparse, urlencode, urljoin
from response import Response
from exceptions import TimeoutError, ConnectionError, RedirectError, ResponseDecodeError


def create_ssl_connection(host, timeout):
    context = ssl.create_default_context()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    sock = context.wrap_socket(sock, server_hostname=host)
    sock.connect((host, 443))
    return sock


def build_put_request(url, data, headers, cookies):
    if data is None:
        data = ''

    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'

    request = []
    request.append(f"PUT {path} HTTP/1.1\r\n")
    request.append(f"Host: {host}\r\n")
    request.append("Connection: close\r\n")
    request.append(f"Content-Length: {len(data)}\r\n")
    if headers:
        for key, value in headers.items():
            request.append(f"{key}: {value}\r\n")
    if cookies:
        cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])
        request.append(f"Cookie: {cookie_header}\r\n")
    request.append("\r\n")
    request.append(data)
    return ''.join(request)


def get_response(sock):
    response = b""
    while True:
        part = sock.recv(4096)
        if not part:
            break
        response += part
    return response


def handle_redirect(url, response_lines, redirect_count, max_redirects):
    if redirect_count >= max_redirects:
        raise RedirectError("Too many redirects")

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
            new_url = urljoin(url, new_url)
        return new_url
    return None


def decode_response(response):
    try:
        response_str = response.decode("utf-8", errors="replace")
    except UnicodeDecodeError:
        raise ResponseDecodeError("Failed to decode response")

    return response_str


def extract_status_and_headers(response_str):
    response_lines = response_str.splitlines()

    if not response_lines:
        raise ResponseDecodeError("Empty response lines.")

    status_line = response_lines[0]
    try:
        status_code = int(status_line.split()[1])
    except (IndexError, ValueError):
        raise ResponseDecodeError(f"Invalid status line: {status_line}")

    response_headers = {}
    for line in response_lines[1:]:
        if line == '':
            break
        try:
            key, value = line.split(': ', 1)
            response_headers[key] = value
        except ValueError:
            continue

    return status_code, response_headers, response_lines


def extract_body(response_str):
    if "\r\n\r\n" in response_str:
        return response_str.split("\r\n\r\n", 1)[1]
    return ""


def http_put(url, data=None, headers=None, cookies=None, timeout=1000, max_redirects=5):
    redirect_count = 0
    while redirect_count < max_redirects:
        try:
            if data is None:
                data = ''

            parsed_url = urlparse(url)
            host = parsed_url.netloc
            sock = create_ssl_connection(host, timeout)

            request = build_put_request(url, data, headers, cookies)
            sock.sendall(request.encode())

            response = get_response(sock)
            sock.close()

            response_str = decode_response(response)

            status_code, response_headers, response_lines = extract_status_and_headers(response_str)

            new_url = handle_redirect(url, response_lines, redirect_count, max_redirects)
            if new_url:
                url = new_url
                redirect_count += 1
                continue

            content = extract_body(response_str)
            return Response(content, status_code, response_headers)

        except (socket.timeout, ConnectionError) as e:
            raise e
        except Exception as e:
            raise ConnectionError(f"An error occurred: {e}")

    raise RedirectError("Too many redirects")