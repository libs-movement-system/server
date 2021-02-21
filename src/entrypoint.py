#!/usr/bin/env python3
"""Entrypoint for systemd."""

import atexit
import logging
from threading import Thread

import movement_system
import server

logging.basicConfig(
    format="{asctime} {levelname}: {message}", style="{", level=logging.INFO, datefmt="%m/%d/%Y %I:%M:%S %p"
)

atexit.register(movement_system.cleanup)

movement_system_thread = Thread(target=movement_system.run, daemon=True)
movement_system_thread.start()
logging.info("Movement system thread started.")

server.serve()
