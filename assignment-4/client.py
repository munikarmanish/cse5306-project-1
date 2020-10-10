# author: Hamza Reza Pavel, Manish Munikar

import json
import socket
import sys
import threading

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


class AsyncRPC:
    def __init__(self, function, args):
        # Assign the argument to the instance's name attribute
        self.function = function
        self.args = args
        self.rpc_type = RPC_ASYNC
        self.computation_id = None
        self.result = None

    def invoke(self):
        """
        Client stub
        """
        # pack the parameters
        request = {
            "function": self.function,
            "args": self.args,
            "rpc_type": self.rpc_type,
            "request_type": REQUEST_INVOKE,
        }

        # send the request and get the reply
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, SERVER_PORT))
        sock.send(json.dumps(request).encode())
        response = sock.recv(65536).decode()

        # parse the response
        response = json.loads(response)
        sock.close()

        if "error" in response:
            raise RuntimeError(response["error"])

        if "response_type" not in response:
            raise RuntimeError("No response type received from server")

        self.computation_id = response["token"]

    def get_result(self):
        request = {
            "rpc_type": self.rpc_type,
            "token": self.computation_id,
            "request_type": REQUEST_RESULT,
        }

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((SERVER_IP, SERVER_PORT))
        sock.send(json.dumps(request).encode())
        response = sock.recv(65536).decode()

        # parse the response
        response = json.loads(response)
        sock.close()
        if "error" in response:
            raise RuntimeError(response["error"])
        if "response_type" not in response:
            raise ValueError("No response type received from server")

        self.result = response["result"]
        return self.result


class DeferredRPC:
    def __init__(self, function, args):
        # Assign the argument to the instance's name attribute
        self.function = function
        self.args = args
        self.rpc_type = RPC_DEFERRED
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((SERVER_IP, SERVER_PORT))

    def __del__(self):
        self.sock.close()

    def get_result(self):
        # wait for response
        response = self.sock.recv(65536).decode()

        # parse the response
        response = json.loads(response)
        if "error" in response:
            raise RuntimeError(response["error"])
        if "response_type" not in response:
            raise RuntimeError("no response type received from server")

        result = response.get("result")
        if result is None:
            raise RuntimeError("error parsing result")
        return response["result"]

    def invoke(self, parallel_function=None, args=[]):
        # pack the parameters
        request = {
            "function": self.function,
            "args": self.args,
            "rpc_type": self.rpc_type,
            "request_type": REQUEST_INVOKE,
        }
        # send the request and get the reply
        self.sock.send(json.dumps(request).encode())

        # do something else while the server is computing the result
        if parallel_function is not None:
            thread = threading.Thread(target=parallel_function, args=args)
            thread.start()

        result = self.get_result()
        print(f"received result from the server: {result}")
        thread.join()
        return result
