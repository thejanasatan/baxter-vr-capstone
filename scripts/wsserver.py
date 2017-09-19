#!/usr/bin/env python

import socket
import time

class WSServer():
  def __init__(self, con_queue, can_queue, host, port):
    self.control_queue = con_queue
    self.cancel_queue = can_queue
    self.host = host
    self.port = port

  def sprint(self, message):
    print('[baxter_unity_server] %s' % message)

  def listen(self):
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.conn.bind((self.host, int(self.port)))

    self.sprint('Server Listening on %s:%s' % (self.host, self.port))

    while True:
      data, addr = self.conn.recvfrom(1024)
      sanitized = self.sanitize_data(data)
      self._publish_command(sanitized[1:]) if sanitized[0] == 'move_arm' else self._publish_cancel(sanitized[1:])

  def sanitize_data(self, data):
    data = [item for item in data.split('|') if item]
    return data

  def _publish_cancel(self, message):
    message = {
      'timestamp': time.time(),
      'type': 'cancel',
      'limb': message[0],
      'goal': message[1]
    }
    self.cancel_queue.put_nowait(message)
    self.sprint('message passed')

  def _publish_command(self, message):
    message = {
        'timestamp': time.time(),
        'type': 'control',
        'limb': message[0],
        'position': message[1],
        'rotation': message[2]
    }
    self.control_queue.put_nowait(message)
    self.sprint('message passed')
