#!/usr/bin/env python3

import base64
import socket
import sys
from pathlib import Path
from threading import Thread

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8080
BUFFER_SIZE = 65536
CONNECTION_LIMIT = 1024


class WorkerThread(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.client_ip = ip
        self.client_port = port
        self.conn = conn
        # print(f"New thread started for client address: {ip}:{port}")

    def run(self):
        data = self.conn.recv(BUFFER_SIZE)
        message = data.decode()
        tokens = message.split("\n")
        command = tokens[0].strip().lower()

        if command == "upload":
            filename = tokens[1].strip()
            encoded = tokens[2].strip().encode()
            file_data = base64.b64decode(encoded)
            Path("uploads/").mkdir(parents=True, exist_ok=True)
            Path("uploads/{}".format(filename)).write_bytes(file_data)
            print(f"Uploaded '{filename}'")

        elif command == "download":
            filename = tokens[1].strip()
            file = Path("uploads/{}".format(filename))
            if file.is_file():
                self.conn.sendto(file.read_bytes(), (self.client_ip, self.client_port))
                print(f"Downloaded '{filename}'")

        elif command == "delete":
            filename = tokens[1].strip()
            file = Path("uploads/{}".format(filename))
            if file.is_file():
                file.unlink()
                print(f"Deleted '{filename}'")

        elif command == "rename":
            filename = tokens[1].strip()
            new_filename = tokens[2].strip()
            file = Path("uploads/{}".format(filename))
            new_file = Path("uploads/{}".format(new_filename))
            if file.is_file():
                file.rename(new_file)
                print(f"Renamed '{filename}' to '{new_filename}'")


def main():
    tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpsock.bind((SERVER_IP, SERVER_PORT))
    print("Server running. Waiting for connection...")
    tcpsock.listen(CONNECTION_LIMIT)
    while True:
        (conn, (client_ip, client_port)) = tcpsock.accept()
        # print(f"Connection request from {client_ip}:{client_port}")
        worker = WorkerThread(client_ip, client_port, conn)
        worker.start()


if __name__ == "__main__":
    main()
