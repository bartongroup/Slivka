import os
import pickle
import sys
import uuid

from socket import socket, AF_INET, SOCK_STREAM

sys.path[0] = os.getcwd()


HOST = 'localhost'
PORT = 9090


class Worker:

    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self._server_socket = socket(family=AF_INET, type=SOCK_STREAM)
        self._server_socket.bind((host, port))
        # self._server_socket.setblocking(False)
        self._server_socket.listen(5)

    def start(self):
        (conn, address) = self._server_socket.accept()
        print("Accepted connection from {}".format(address))

        runnable_string = conn.recv(4096)
        conn.send(b'\x00')
        args_string = conn.recv(4096)
        conn.send(b'\x00')
        kwargs_string = conn.recv(4096)
        conn.send(b'\x00')

        runnable = pickle.loads(runnable_string)
        args = pickle.loads(args_string)
        kwargs = pickle.loads(kwargs_string)

        conn.send(b'OK\x00\x00')

        job_id = self._do_work(runnable, args, kwargs)
        conn.send(job_id.encode())
        conn.close()

    def _start_job(self, callable, args, kwargs):
        print("Starting <{}> with args {} and kwargs {}"
              .format(callable.__name__, args, kwargs))

        return uuid.uuid4().hex


if __name__ == '__main__':
    w = Worker()
    w.start()