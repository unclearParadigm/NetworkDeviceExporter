#!/usr/bin/env python3

from http.server import HTTPServer, BaseHTTPRequestHandler

import configuration
from requesthandler import RequestHandler


def http_run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = (configuration.ListenAddress, configuration.ListenPort)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    print("Starting NDE on 'http://{0}:{1}/'".format(configuration.ListenAddress, configuration.ListenPort))

    try:
        http_run(HTTPServer, RequestHandler)
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(exc)

    print("NDE stopped")
