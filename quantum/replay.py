#!/bin/env python3

import socket

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
                print(f'Connected by {addr}')
                data = conn.recv(1024)
                if not data:
                    break

                response_body = data.decode('utf-8', errors='replace')

                response_header = (
                    "HTTP/1.1 302 FOUND\r\n"
                    "Location: http://127.0.0.1"
                    "Content-type: text/plain\r\n"
                    f"Content-Lenght: {len(response_body)}\r\n"
                    "Connection: close\r\n"
                    "\r\n"
                )

                conn.sendall(response_header.encode('utf-8') + response_body.encode('utf-8'))
    except KeyboardInterrupt:
        print("\nServer is shutting down...")
        s.close()
        exit(1)