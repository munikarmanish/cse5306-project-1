#!/usr/bin/env python3

import json
import socket
import sys

import numpy as np

SERVER_IP = "0.0.0.0"
SERVER_PORT = 8080


def send_error(connection, msg):
    reply = json.dumps({"error": msg})
    connection.send(reply.encode())


def calculate_pi():
    return 3.14


def add(x, y):
    return x + y


def sort(array):
    return sorted(array)


def matrix_multiply(A, B):
    return np.dot(np.array(A), np.array(B)).tolist()


def rpc(connection, request):
    """ Server stub """
    # unpack the parameters
    request = json.loads(request)

    # call the actual function
    f = globals().get(request["function"])
    if not f:
        send_error(connection, "invalid function")
        return
    try:
        result = f(*request["args"])
        # send the result back
        reply = json.dumps({"result": result})
        connection.send(reply.encode())
    except Exception:
        send_error(connection, "error while executing function")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(5)
    while True:
        connection, _sender_address = sock.accept()
        request = connection.recv(65536).decode()
        rpc(connection, request)
        connection.close()


if __name__ == "__main__":
    main()
