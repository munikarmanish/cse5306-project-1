#!/usr/bin/env python3

import select
import socket
import sys
from pathlib import Path

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
BUFFER_SIZE = 65536


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
        args["filename"] = sys.argv[2].strip()
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
            args["new_filename"] = sys.argv[3].strip()
        except IndexError:
            abort("new filename not provided")
    else:
        abort("invalid command")

    return args


def do_upload(sock, filename):
    file = Path(filename)
    if not file.is_file():
        abort("invalid file")
    data = file.read_bytes()
    command = bytearray("{}\n{}\n".format("UPLOAD", file.name).encode())
    msg = command + data
    sock.send(msg)


def do_download(sock, filename):
    msg = "{}\n{}".format("DOWNLOAD", filename)
    sock.send(msg.encode())
    ready = select.select([sock], [], [], 1)[0]
    if ready:
        data, _sender = sock.recvfrom(BUFFER_SIZE)
        Path("downloads/").mkdir(parents=True, exist_ok=True)
        Path("downloads/{}".format(filename)).write_bytes(data)
    else:
        abort("download timeout")


def do_delete(sock, filename):
    msg = "{}\n{}".format("DELETE", filename)
    sock.send(msg.encode())


def do_rename(sock, filename, new_filename):
    msg = "{}\n{}\n{}".format("RENAME", filename, new_filename)
    sock.send(msg.encode())


def main():
    args = parse_arguments()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    if args["command"] == "upload":
        do_upload(sock, args["filename"])
    elif args["command"] == "download":
        do_download(sock, args["filename"])
    elif args["command"] == "delete":
        do_delete(sock, args["filename"])
    elif args["command"] == "rename":
        do_rename(sock, args["filename"], args["new_filename"])
    sock.close()


if __name__ == "__main__":
    main()
