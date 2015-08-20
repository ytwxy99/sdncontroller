# -*- coding: utf-8 -*-

import socket

def create_new_socket():
    """Get a socket hock """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(block)
    return sock
	
