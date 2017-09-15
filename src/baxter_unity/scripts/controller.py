#!/usr/bin/env python

import argparse, sys
from multiprocessing import Process
from Queue import Queue

from baxter_unity import WSServer
from baxter_unity import BaxterNode

def start_node_server(host, port):
    
    # Control Message Queue and Cancel Message Queue
    control_queue = Queue()
    cancel_queue = Queue()

    # setup concurrent process for ws_server
    ws = WSServer(control_queue, cancel_queue, host, port)
    ws_process = Process(target=ws.listen, args=())
    
    # setup concurrent process for control_node
    cn = BaxterNode(control_queue, cancel_queue)
    cn_process = Process(target=cn.start, args=())

    ws_process.start()
    cn_process.start()

def main():
    """
    Argument Parser to process the arguments passed into the controller
    """
    arg_fmt = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt)

    parser.add_argument(
        "-p", "--port", dest="port", default="5005", 
        help="Port that the Websocket server is listening on"
    )

    parser.add_argument(
        "-h", "--host", dest="host", default="0.0.0.0",
        help="IP that the Websocket server is listening on"
    )

    args = parser.parse_args(rospy.myargv()[1:])
    start_node_server(args.host, args.port)


if __name__ == '__main__':
    sys.exit(main())