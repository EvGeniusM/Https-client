import socket
import ssl
from urllib.parse import urlparse, urlencode, urljoin
from response import Response
from exceptions import TimeoutError, ConnectionError, RedirectError, ResponseDecodeError

def http_post(url, data=None, headers=None, cookies=None, timeout=1000, max_redirects=5):
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'

    if data:
        data = urlencode(data)
    else:
        data = ''

    context = ssl.create_default_context()
    redirect_count = 0

    while redirect_count < max_redirects:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock = context.wrap_socket(sock, server_hostname=host)

        request = []

        try:
            sock.connect((host, 443))
            request.append(f"POST {path} HTTP/1.1\r\n")
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
            request = ''.join(request)

            sock.sendall(request.encode())

            response = b""
            while True:
                part = sock.recv(4096)
                if not part:
                    break
                response += part

        except socket.timeout:
            raise TimeoutError()
        except Exception as e:
            raise ConnectionError(f"An error occurred: {e}")
        finally:
            sock.close()

        try:
            response_str = response.decode('utf-8', errors='replace')
        except UnicodeDecodeError:
            raise ResponseDecodeError("Failed to decode response using UTF-8")

        response_lines = response_str.splitlines()
        status_line = response_lines[0]
        status_code = int(status_line.split()[1])

        headers = {}
        for line in response_lines[1:]:
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
            content = response.decode(encoding, errors='replace').split("\r\n\r\n", 1)[1]
        except (UnicodeDecodeError, LookupError):
            raise ResponseDecodeError(f"Unknown encoding '{encoding}'")

        if status_code in (301, 302, 303, 307, 308):
            if 'Location' in headers:
                new_url = headers['Location']
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

        if redirect_count >= max_redirects:
            raise RedirectError()

        break

    return Response(content, status_code, headers)

def save_response_to_file(response, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.get_content())