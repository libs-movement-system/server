"""TCP server"""

__all__ = ["run"]

import json
import socketserver
from typing import Any, Callable, Dict

SERVER_ADDRESS = ("raspberrypi.local", 35007)


def run(handler: Callable[[Dict], Any]) -> None:
    """Runs the handler function with incoming JSON
    data (a dict) as the sole positional argument.

    :param handler: handler function
    :type handler: Callable[[Dict], Any]
    """
    RequestHandler.user_handler = handler

    with LoggingTCPServer(SERVER_ADDRESS, RequestHandler) as server:
        # Will keep running until interrupted with Ctrl-C
        server.serve_forever()


class RequestHandler(socketserver.BaseRequestHandler):
    """The request handler for this TCP server. This overrides the handle()
    method to implement handling of incoming communication from the client.

    Note that the actual function used to handle requests is monkey-patched at runtime as
    that was the only way I could think of to deal with user-provided handler functions.
    """

    user_handler = None  # The user handler is set in the run function.

    def setup(self) -> None:
        print(f"Will handle new request from {self.client_address}.")

    def handle(self) -> None:
        """Handle requests. Basically just load JSON from text of data and pass it into
        user-provided handler function.
        """
        self.data = self.request.recv(1024)
        self.data = json.loads(self.data)

        RequestHandler.user_handler(self.data)

    def finish(self) -> None:
        print(f"Handled {self.data} from {self.client_address}.")


class LoggingTCPServer(socketserver.TCPServer):
    def server_activate(self):
        """Same as overridden method just with logging"""
        self.socket.listen()
        print("Server is up.")
