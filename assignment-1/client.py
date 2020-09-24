#!/usr/bin/env python3

import base64
import select
import socket
import sys
from pathlib import Path

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080


def abort(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def parse_arguments():
    args = {}

    # get command
    try:
        args["command"] = sys.argv[1].strip().lower()
    except IndexError:
        abort("no command provided")

    # get filename
    try:
        args["filename"] = sys.argv[2].strip().lower()
    except IndexError:
        abort("no filename provided")

    if args["command"] == "upload":
        pass
    elif args["command"] == "download":
        pass
    elif args["command"] == "delete":
        pass
    elif args["command"] == "rename":
        # get new filename
        try:
            args["new_filename"] = sys.argv[3].strip().lower()
        except IndexError:
            abort("new filename not provided")
    else:
        abort("invalid command")

    return args


def do_upload(sock, filename):
    file = Path(filename)
    if not file.is_file():
        abort("invalid file")
    encoded = base64.b64encode(file.read_bytes()).decode()
    msg = "{}\n{}\n{}".format("UPLOAD", file.name, encoded)
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))


def do_download(sock, filename):
    msg = "{}\n{}".format("DOWNLOAD", filename)
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))
    ready = select.select([sock], [], [], 1)[0]
    if ready:
        data, _sender = sock.recvfrom(65536)
        Path("downloads/").mkdir(parents=True, exist_ok=True)
        Path("downloads/{}".format(filename)).write_bytes(data)
    else:
        abort("download timeout")


def do_delete(sock, filename):
    msg = "{}\n{}".format("DELETE", filename)
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))


def do_rename(sock, filename, new_filename):
    msg = "{}\n{}\n{}".format("RENAME", filename, new_filename)
    sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT))


def main():
    args = parse_arguments()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    if args["command"] == "upload":
        do_upload(sock, args["filename"])
    elif args["command"] == "download":
        do_download(sock, args["filename"])
    elif args["command"] == "delete":
        do_delete(sock, args["filename"])
    elif args["command"] == "rename":
        do_rename(sock, args["filename"], args["new_filename"])


if __name__ == "__main__":
    main()
