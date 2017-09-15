#!/usr/bin/env python

import socket
from re import split

class WSServer():
    def __init__(self, con_queue, can_queue, host, port):
        self.control_queue = con_queue
        self.cancel_queue = can_queue
        self.host = host
        self.port = port
        self.last_goal = int(-inf)

    def sprint(self, message):
        print('[baxter_unity_server] %s' % message)

    def listen(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.conn.bind((self.host, self.port))

        self.sprint('Server Listening on %s:%s' % (self.host, self.port))

        while True:
            data, addr = self.conn.recvfrom(1024)
            sanitize_data(data)
            self.sprint("received message %s" % data)

    def sanitize_data(self, data):
        data = [item for item in split('|', data) if item]
        return data