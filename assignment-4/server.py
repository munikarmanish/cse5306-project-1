# author: Hamza Reza Pavel, Manish Munikar

import json
import socket
import random
import numpy as np

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080

# rpc_type
RPC_SYNC = 0
RPC_ASYNC = 1
RPC_DEFERRED = 2

# request_type
REQUEST_INVOKE = 1
REQUEST_RESULT = 2

# response_type
RESPONSE_ACK = 1
RESPONSE_RESULT = 2

# global result table
RESULTS = dict()


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


def process_rpc(connection, request):
    request = json.loads(request)
    if "rpc_type" not in request:
        send_error(connection, "no rpc type sent in last message")
    if request["rpc_type"] == RPC_ASYNC:
        process_async_rpc(connection, request)
    elif request["rpc_type"] == RPC_DEFERRED:
        process_deferred_rpc(connection, request)


def process_async_rpc(connection, request):
    if request["request_type"] == REQUEST_INVOKE:
        token = random.randint(1, 10000)
        f = globals().get(request["function"])
        if not f:
            send_error(connection, "invalid function")
            return
        reply = json.dumps({"response_type": RESPONSE_ACK, "token": token})
        connection.send(reply.encode())
        try:
            result = f(*request["args"])
            RESULTS[token] = result
        except Exception:
            send_error(connection, "error while executing function")
    elif request["request_type"] == REQUEST_RESULT:
        token = int(request["token"])
        result = RESULTS[token]
        reply = json.dumps({"result": result, "response_type": RESPONSE_RESULT})
        connection.send(reply.encode())
    else:
        send_error(connection, "invalid request type")


def process_deferred_rpc(connection, request):
    f = globals().get(request["function"])
    if not f:
        send_error(connection, "invalid function")
        return
    try:
        result = f(*request["args"])
        # send the result back
        reply = json.dumps({"result": result, "response_type": RESPONSE_RESULT})
        connection.send(reply.encode())
    except Exception:
        send_error(connection, "error while executing function")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((SERVER_IP, SERVER_PORT))
    sock.listen(10)
    while True:
        connection, _sender_address = sock.accept()
        request = connection.recv(65536).decode()
        process_rpc(connection, request)
        connection.close()


if __name__ == "__main__":
    main()
