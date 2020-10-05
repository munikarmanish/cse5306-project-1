#!/usr/bin/env python3

import json
import socket
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080


def rpc(function, args):
    """ Client stub """
    # pack the parameters
    request = {"function": function, "args": args}

    # send the request and get the reply
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    sock.send(json.dumps(request).encode())
    response = sock.recv(65536).decode()
    sock.close()

    # parse the response
    response = json.loads(response)
    if "error" in response:
        raise RuntimeError(response["error"])
    return response["result"]


def main():
    print("\ncalculate_pi")
    print(rpc("calculate_pi", args=[]))

    print("\nadd(1, 2)")
    print(rpc("add", args=[1,2]))

    print("\nsort([5,4,3,2,1])")
    print(rpc("sort", args=[[5, 4, 3, 2, 1]]))

    print("\nmatrix_multiply([[1,2],[3,4]], [[5,6],[7,8]])")
    print(rpc("matrix_multiply", [
        [[1, 2], [3, 4]],
        [[5, 6], [7, 8]]
    ]))


if __name__ == "__main__":
    main()
