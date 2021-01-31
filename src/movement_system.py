"""Movement controller"""

__all__ = ["run"]

import logging
from time import sleep

import RPi.GPIO as GPIO

import cfg

# TODO: Why necessary?
increment = 5.08 / 400  # Lead screw pitch / steps per rev


# ---- Set up GPIO ----

CW = 1  # Clockwise Rotation
CCW = 0  # Counterclockwise Rotation
DIR_X = 17  # Direction GPIO Pin
STEP_X = 18  # Step GPIO Pin
DIR_Y = 19  # Direction GPIO Pin
STEP_Y = 20  # Step GPIO Pin
DIR_Z = 21  # Direction GPIO Pin
STEP_Z = 22  # Step GPIO Pin
SLEEP = 23  # Sleep GPIO Pin


GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_X, GPIO.OUT)
GPIO.setup(STEP_X, GPIO.OUT)
GPIO.output(DIR_X, CW)
GPIO.setup(DIR_Y, GPIO.OUT)
GPIO.setup(STEP_Y, GPIO.OUT)
GPIO.output(DIR_Y, CW)
GPIO.setup(DIR_Z, GPIO.OUT)
GPIO.setup(STEP_Z, GPIO.OUT)
GPIO.output(DIR_Z, CW)
GPIO.setup(SLEEP, GPIO.OUT)
logging.info("GPIO setup complete.")

# ---- End setup ----


def run() -> None:
    """Receive movement instructions and execute until stopped."""
    x_pos = y_pos = z_pos = 0  # TODO: Do they always start at 0?

    logging.info("Infinite loop starting.")
    while True:
        x_target = cfg.data["x"]
        y_target = cfg.data["y"]
        z_target = cfg.data["z"]

        if (x_pos, y_pos, z_pos) != (x_target, y_target, z_target):
            GPIO.output(SLEEP, GPIO.HIGH)  # TODO: Why necessary?

            x_pos = move_x(x_pos, x_target)
            y_pos = move_y(y_pos, y_target)
            z_pos = move_z(z_pos, z_target)

            sleep(0.005)

            # TODO: Why necessary?
            GPIO.output(STEP_X, GPIO.LOW)
            GPIO.output(STEP_Y, GPIO.LOW)
            GPIO.output(STEP_Z, GPIO.LOW)
        else:
            GPIO.output(SLEEP, GPIO.LOW)  # TODO: Why necessary?


def move_x(x_pos: int, x_target: int) -> int:
    """Move along x-axis one step toward target position. If already there, do nothing."""
    if x_pos < x_target:
        GPIO.output(STEP_X, GPIO.HIGH)
        GPIO.output(DIR_X, CW)
        x_pos += 1
    if x_pos > x_target:
        GPIO.output(STEP_X, GPIO.HIGH)
        GPIO.output(DIR_X, CCW)
        x_pos -= 1
    return x_pos


def move_y(y_pos: int, y_target: int) -> int:
    """Move along y-axis one step toward target position. If already there, do nothing."""
    if y_pos < y_target:
        GPIO.output(STEP_Y, GPIO.HIGH)
        GPIO.output(DIR_Y, CW)
        y_pos += 1
    if y_pos > y_target:
        GPIO.output(STEP_Y, GPIO.HIGH)
        GPIO.output(DIR_Y, CCW)
        y_pos -= 1
    return y_pos


def move_z(z_pos: int, z_target: int) -> int:
    """Move along z-axis one step toward target position. If already there, do nothing."""
    if z_pos < z_target:
        GPIO.output(STEP_Z, GPIO.HIGH)
        GPIO.output(DIR_Z, CW)
        z_pos += 1
    if z_pos > z_target:
        GPIO.output(STEP_Z, GPIO.HIGH)
        GPIO.output(DIR_Z, CCW)
        z_pos -= 1
    return z_pos
