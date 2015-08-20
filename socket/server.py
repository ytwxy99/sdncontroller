# -*- coding: utf-8 -*-

import errno
import functools
import tornado.ioloop as ioloop
import Queue
import time
from sdncontroller.common import utils_socket

def socket_server():
    """Build socket server"""
    
    # To create a new sock object
    sock = utils_socket.create_new_socket(0)
    # Bind sock hook
    sock.bind(("", 6634))
    # To listen request from client service
    sock.listen(30)
    
    # Get a IOLoop instance	
    io_loop = ioloop.IOLoop.instance()

    # Using functools's modal to genrate a callback function	
    callback = functools.partial(agent, sock)
    print sock, sock.getsockname()
    # Add handler by io_loop
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    try: 
        io_loop.start()
    except KeyboardInterrupt: 
        io_loop.stop()
        print "quit"

if __name__ == '__main__':
    socket_server()
