#!/usr/bin/env python3
"""Run by systemd so the movement system is daemonized."""

import sys

import app
import server

try:
    server.run(app.handler)
except KeyboardInterrupt:
    print("Ctrl-C interrupted execution.", file=sys.stderr)
