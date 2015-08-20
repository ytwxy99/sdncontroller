# -*- coding: utf-8 -*-

import functools
import tornado.ioloop as ioloop
from sdncontroller.common import utils_socket

def socket_server():
    """Build socket server"""
    
    # To create a new sock object
    sock = utils_socket.create_new_socket(0)
    # Bind sock hook
    sock.bind(("", 6634))
    # To listen request from client service
    sock.listen(30)
    
    #print sock, sock.getsockname()
    # Get a IOLoop instance	
    io_loop = ioloop.IOLoop.instance()

    # Using functools's modal to genrate a callback function	
    callback = functools.partial(socket_server_accept, sock, io_loop)
    # Help information: add_handler(self, fd, handler, events) from help(io_loop)
    # Add handler by io_loop
    io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
    try: 
        # Start IO loop
        io_loop.start()
    except KeyboardInterrupt: 
        # Stop IO loop
        io_loop.stop()
        print "\n Quite"

def socket_server_accept(sock, io_loop, fd, events):
    print fd, sock, events
    try:
        connection, address = sock.accept()
    except socket.error, e:
        if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
            raise
        return
    connection.setblocking(0)
    handle_connection(connection, address)
    fd_map[connection.fileno()] = connection
    client_handle = functools.partial(client_handler, address)
    io_loop.add_handler(connection.fileno(), client_handle, io_loop.READ)
    print "i n agent: new switch", connection.fileno(), client_handle
    message_queue_map[connection] = Queue.Queue()

if __name__ == '__main__':
    socket_server()
