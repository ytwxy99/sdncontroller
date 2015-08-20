# -*- coding: utf-8 -*-

import functools
import tornado.ioloop as ioloop
from sdncontroller.common import utils_socket
import errno
import functools
import socket
import Queue
import time

message_queue_map = dict()

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
    """socket's acception service"""
    #print fd, sock, events
    try:
        # Get connection and address
        connection, address = sock.accept()
    except socket.error, e:
        if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
            raise
        return
    connection.setblocking(0)
    # Do handle_connection function
    handle_connection(connection, address)
    # Set connection into fd_map
    fd_map[connection.fileno()] = connection
    # Using functools's modal to genrate a callback function which is client_handle
    client_handle = functools.partial(client_handler, address, io_loop, fd_map)
    # Add handler by io_loop
    io_loop.add_handler(connection.fileno(), client_handle, io_loop.READ)
    # print some information
    print "i n agent: new switch", connection.fileno(), client_handle
    message_queue_map[connection] = Queue.Queue()

def handle_connection(connection, address):
    """Print connection and address informations"""
    print "1 connection,", connection, address

def client_handler(address, io_loop, fd_map, fd, events):
    """The handler for acception data """
    # Get sock from fd_map by fd
    sock = fd_map[fd]
    # Ensure io_loop and events are 'READ'
    if events & io_loop.READ:
        # Get 1024 byte data
        data = sock.recv(1024)
        #非阻塞情况下如果收到的是空数据，则取消句柄
        if data == '':
            print "connection dropped"
            # Remove hook if data is none
            io_loop.remove_handler(fd)
        #openflow报文最短是8字节，即报头8字节
        if len(data)<8:
            print "not a openflow message"
        else:
            if len(data)>8:
                rmsg = of.ofp_header(data[0:8])  #封装ofp_header
                body = data[8:]
            else:  
                rmsg = of.ofp_header(data)
            msg = of.ofp_header(type = 0,xid = rmsg.xid)   
            message_queue_map[sock].put(str(msg))
            # Modified IO loop status
            io_loop.update_handler(fd, io_loop.WRITE)

    # Ensure io_loop and events are 'Write'
    if events & io_loop.WRITE:
        try:
            # Get informations from queue
            next_msg = message_queue_map[sock].get_nowait()
        except Queue.Empty:
            io_loop.update_handler(fd, io_loop.READ)#取完数据之后恢复可读状态，等待数据。
        else:
            #print 'sending "%s" to %s' % (of.ofp_header(next_msg).type,    address)
            sock.send(next_msg)#发送给dpid

if __name__ == '__main__':
    socket_server()
