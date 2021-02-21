"""TCP server"""

__all__ = ["serve"]

import json
import logging
import socketserver

import data

SERVER_ADDRESS = ("raspberrypi.local", 35007)


def serve() -> None:
    """Run TCP server."""
    with LoggingTCPServer(SERVER_ADDRESS, RequestHandler) as server:
        # Will keep running until interrupted with Ctrl-C
        server.serve_forever()


class RequestHandler(socketserver.BaseRequestHandler):
    def setup(self) -> None:
        logging.info(f"Will handle request from {self.client_address}. Current targets: {data.targets}")

    def handle(self) -> None:
        """Load JSON from received string and update global data"""
        data_str = self.request.recv(1024)
        data.targets = json.loads(data_str)

    def finish(self) -> None:
        logging.info(f"Handled request from {self.client_address}. New targets: {data.targets}")


class LoggingTCPServer(socketserver.TCPServer):
    def server_activate(self) -> None:
        """Same as overridden method just with logging"""
        self.socket.listen()
        logging.info("Server activated.")
