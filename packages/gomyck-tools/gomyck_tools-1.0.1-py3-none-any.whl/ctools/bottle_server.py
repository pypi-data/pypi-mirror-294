from bottle import ServerAdapter
from socketserver import ThreadingMixIn
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler, make_server
from geventwebsocket.handler import WebSocketHandler
from ctools import sys_log

class ThreadedWSGIServer(ThreadingMixIn, WSGIServer): pass

class CustomWSGIHandler(WSGIRequestHandler):
  def log_request(*args, **kw): pass

class CustomWebSocketHandler(WebSocketHandler):
  def log_request(self):
    if '101' not in str(self.status):
      log_msg = self.format_request()
      for nk in sys_log.neglect_keywords:
        if nk in log_msg:
          return
      self.logger.info(log_msg)

class WSGIRefServer(ServerAdapter):

  def __init__(self, host='0.0.0.0', port=8010):
    super().__init__(host, port)
    self.server = None

  def run(self, handler):
    req_handler = WSGIRequestHandler
    if self.quiet: req_handler = CustomWSGIHandler
    self.server = make_server(self.host, self.port, handler, server_class=ThreadedWSGIServer, handler_class=req_handler)
    self.server.serve_forever()

  def stop(self):
    self.server.shutdown()


class WebSocketServer(ServerAdapter):

  def __init__(self, host='0.0.0.0', port=8012):
    super().__init__(host, port)
    self.server = None

  def run(self, handler):
    from gevent import pywsgi
    self.server = pywsgi.WSGIServer((self.host, self.port), handler, handler_class=CustomWebSocketHandler)
    self.server.serve_forever()

  def stop(self):
    self.server.stop()
