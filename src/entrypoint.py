#!/usr/bin/env python3
"""Entrypoint for systemd."""

import logging
import sys
from threading import Thread

import movement_system
import server

try:
    logging.basicConfig(format="{name}: {message}", style="{", level=logging.INFO)

    movement_system_thread = Thread(target=movement_system.run, daemon=True)
    movement_system_thread.start()
    logging.info("Movement system thread started.")

    server.serve()
except KeyboardInterrupt:
    logging.critical("Ctrl-C interrupted execution.")
    sys.exit(1)
