import socket
import ssl
from urllib.parse import urlparse, urlencode, urljoin
from response import Response
from exceptions import TimeoutError, ConnectionError, RedirectError, ResponseDecodeError


def parse_url(url):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'
    return host, path


def build_request(host, path, data, headers, cookies):
    request = [
        f"POST {path} HTTP/1.1\r\n",
        f"Host: {host}\r\n",
        "Connection: close\r\n",
        f"Content-Length: {len(data)}\r\n"
    ]

    if headers:
        request.extend(f"{key}: {value}\r\n" for key, value in headers.items())

    if cookies:
        cookie_header = '; '.join(f"{key}={value}" for key, value in cookies.items())
        request.append(f"Cookie: {cookie_header}\r\n")

    request.extend(["\r\n", data])
    return ''.join(request)


def send_request(host, request, timeout):
    context = ssl.create_default_context()
    with socket.create_connection((host, 443), timeout) as sock:
        sock = context.wrap_socket(sock, server_hostname=host)
        sock.sendall(request.encode())
        response = b""
        while True:
            part = sock.recv(4096)
            if not part:
                break
            response += part
    return response


def parse_response(response_bytes):
    try:
        response_str = response_bytes.decode('utf-8', errors='replace')
    except UnicodeDecodeError:
        raise ResponseDecodeError("Failed to decode response using UTF-8")

    lines = response_str.splitlines()
    status_line = lines[0]
    status_code = int(status_line.split()[1])

    headers = {}
    for line in lines[1:]:
        if line == '':
            break
        try:
            key, value = line.split(': ', 1)
            headers[key] = value
        except ValueError:
            continue

    content_type = headers.get('Content-Type', '')
    encoding = 'utf-8'
    if 'charset=' in content_type:
        encoding = content_type.split('charset=')[-1].strip()

    try:
        content = response_str.split("\r\n\r\n", 1)[1]
    except IndexError:
        content = ""

    return Response(content, status_code, headers)


def handle_redirects(url, headers, redirect_count, max_redirects):
    if 'Location' in headers:
        new_url = headers['Location']
        if not new_url.startswith('http'):
            new_url = urljoin(url, new_url)
        return new_url, redirect_count + 1
    return url, redirect_count


def http_post(url, data=None, headers=None, cookies=None, timeout=1000, max_redirects=5):
    if data:
        data = urlencode(data)
    else:
        data = ''

    redirect_count = 0

    while redirect_count < max_redirects:
        host, path = parse_url(url)
        request = build_request(host, path, data, headers, cookies)

        try:
            response_bytes = send_request(host, request, timeout)
            response = parse_response(response_bytes)
        except socket.timeout:
            raise TimeoutError()
        except Exception as e:
            raise ConnectionError(f"An error occurred: {e}")

        status_code = response.status_code
        if status_code in (301, 302, 303, 307, 308):
            url, redirect_count = handle_redirects(url, response.headers, redirect_count, max_redirects)
            continue

        if redirect_count >= max_redirects:
            raise RedirectError()

        return response

    raise RedirectError()


def save_response_to_file(response, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.get_content())