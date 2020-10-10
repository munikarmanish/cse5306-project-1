#!/usr/bin/python3

import socket
import sys
from pathlib import Path

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8080
BUFFER_SIZE = 65536
CONNECTION_LIMIT = 10


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(CONNECTION_LIMIT)
    print(f"Server running at {SERVER_IP}:{SERVER_PORT}")

    while True:
        conn, (ip,port) = sock.accept()
        msg = conn.recv(BUFFER_SIZE)
        tokens = msg.split(b"\n", maxsplit=2)
        command = tokens[0].decode().strip().lower()

        if command == "upload":
            filename = tokens[1].decode().strip()
            file_data = tokens[2]
            Path("uploads/").mkdir(parents=True, exist_ok=True)
            Path("uploads/{}".format(filename)).write_bytes(file_data)
            print(f"{ip}:{port} - Uploaded '{filename}'")

        elif command == "download":
            filename = tokens[1].decode().strip()
            file = Path("uploads/{}".format(filename))
            if file.is_file():
                conn.send(file.read_bytes())
                print(f"{ip}:{port} - Downloaded '{filename}'")


        elif command == "delete":
            filename = tokens[1].decode().strip()
            file = Path("uploads/{}".format(filename))
            if file.is_file():
                file.unlink()
                print(f"{ip}:{port} - Deleted '{filename}'")

        elif command == "rename":
            filename = tokens[1].decode().strip()
            new_filename = tokens[2].decode().strip()
            file = Path("uploads/{}".format(filename))
            new_file = Path("uploads/{}".format(new_filename))
            if file.is_file():
                file.rename(new_file)
                print(f"{ip}:{port} - Renamed '{filename}' to '{new_filename}'")


if __name__ == "__main__":
    main()
