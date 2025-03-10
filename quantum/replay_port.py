#!/bin/env python

import socket
from urllib.parse import urlparse, parse_qs

HOST = '0.0.0.0'
PORT = 5000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server is listening on {HOST}:{PORT}')

    try:
        while True:
            conn, addr = s.accept()
            with conn:
                #print(f'Connected by {addr}')
                data = conn.recv(1024)
                if not data:
                    break
                
                request_text = data.decode('utf-8', errors='replace')
                # Разбиваем запрос на строки и извлекаем первую (например: "GET /?port=8080 HTTP/1.1")
                request_lines = request_text.splitlines()
                if request_lines:
                    request_line = request_lines[0]
                    parts = request_line.split()
                    if len(parts) >= 2:
                        method = parts[0]
                        path = parts[1]
                    else:
                        method = ''
                        path = ''
                else:
                    method = ''
                    path = ''

                # Инициализируем переменную для параметра port
                port_value = ''
                response_body = ''

                # Если метод GET, парсим URL и извлекаем параметр port
                if method.upper() == 'GET':
                    parsed_url = urlparse(path)
                    params = parse_qs(parsed_url.query)
                    # Извлекаем значение параметра "name", если он присутствует (иначе будет пустая строка)
                    port_value = params.get('port', [''])[0]
                    url_value = params.get('url', [''])[0]

                response_header = (
                    "HTTP/1.1 302 FOUND\r\n"
                    "Content-Type: text/plain\r\n"
                    f"Location: http://localhost:{port_value}/{url_value}\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )
                
                print(f'Connectd by {addr} used port: {port_value} / path={url_value}')
                print(f'Location: http://localhost:{port_value}/{url_value}')

                conn.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
        s.close()
        exit(1)