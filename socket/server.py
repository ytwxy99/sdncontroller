# -*- coding: utf-8 -*-

import errno
import functools
import tornado.ioloop as ioloop
import Queue
import time
from sdncontroller.common import utils_socket

if __name__ == '__main__':
	sock = utils_socket.create_new_socket(0)
	sock.bind(("", 6634))
	sock.listen(30)
	
	io_loop = ioloop.IOLoop.instance()
	
	callback = functools.partial(agent, sock)
	print sock, sock.getsockname()
	io_loop.add_handler(sock.fileno(), callback, io_loop.READ)
	try:
		io_loop.start()
	except KeyboardInterrupt:
		io_loop.stop()
		print "quit"
