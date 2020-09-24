#!/usr/bin/python3

import base64
import socket
import sys
from pathlib import Path

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8080


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((SERVER_IP, SERVER_PORT))

    while True:
        data, sender_address = sock.recvfrom(1024)
        message = data.decode()
        tokens = message.split("\n")
        command = tokens[0].strip().lower()

        if command == "upload":
            filename = tokens[1].strip()
            encoded = tokens[2].strip().encode()
            file_data = base64.b64decode(encoded)
            Path("uploads/").mkdir(parents=True, exist_ok=True)
            Path("uploads/{}".format(filename)).write_bytes(file_data)
        elif command == "download":
            filename = tokens[1].strip()
            file = Path("uploads/{}".format(filename))
            if not file.is_file():
                pass
            sock.sendto(file.read_bytes(), sender_address)
        elif command == "delete":
            filename = tokens[1].strip()
            file = Path("uploads/{}".format(filename))
            if file.is_file():
                file.unlink()
        elif command == "rename":
            filename = tokens[1].strip()
            new_filename = tokens[2].strip()
            file = Path("uploads/{}".format(filename))
            new_file = Path("uploads/{}".format(new_filename))
            if file.is_file():
                file.rename(new_file)


if __name__ == "__main__":
    main()
