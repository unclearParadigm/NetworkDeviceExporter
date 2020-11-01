import constants
import socketserver

from typing import Tuple
from http.server import BaseHTTPRequestHandler

from metricsprovider import MetricsProvider


class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request: bytes, client_address: Tuple[str, int], server: socketserver.BaseServer):
        super().__init__(request, client_address, server)

    # noinspection PyPep8Naming
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        if self.path == '/metrics':
            response_content = MetricsProvider().collect()
        else:
            response_content = 'Network Device Exporter v{0}'.format(constants.VERSION_STRING)

        self.wfile.write(bytes(response_content, 'utf-8'))
