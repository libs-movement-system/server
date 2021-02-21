"""Movement controller"""

__all__ = ["run", "cleanup"]

import logging
from time import sleep
from typing import Tuple

import RPi.GPIO as GPIO

import data

INCREMENT = 5.08 / 400  # Lead screw pitch / steps per rev

CW = 1  # clockwise rotation
CCW = 0  # counterclockwise rotation

STEP_X = 7  # x-axis step GPIO pin
DIR_X = 8  # x-axis direction GPIO pin

STEP_Y = 10  # y-axis step GPIO pin
DIR_Y = 12  # y-axis direction GPIO pin

STEP_Z = 3  # z-axis step GPIO pin
DIR_Z = 5  # z-axis direction GPIO pin

SLEEP = 15  # sleep GPIO pin


def run() -> None:
    """Receive movement instructions and execute until stopped."""
    setup_gpio()

    x_pos = y_pos = z_pos = 0.0

    logging.info("Infinite loop starting.")
    while True:
        x_target = data.targets["x"]
        y_target = data.targets["y"]
        z_target = data.targets["z"]
        logging.debug(f"Targets: {data.targets}.")

        if not is_in_position((x_pos, y_pos, z_pos), (x_target, y_target, z_target)):
            logging.debug(
                f"Not in position. Current positions: {(x_pos, y_pos, z_pos)}. Current targets: {(x_target, y_target, z_target)}."  # noqa: E501
            )

            GPIO.output(SLEEP, GPIO.HIGH)

            x_pos = move_x(x_pos, x_target)
            y_pos = move_y(y_pos, y_target)
            z_pos = move_z(z_pos, z_target)

            sleep(0.005)

            GPIO.output(STEP_X, GPIO.LOW)
            GPIO.output(STEP_Y, GPIO.LOW)
            GPIO.output(STEP_Z, GPIO.LOW)
        else:
            logging.debug(
                f"In position. Current positions: {(x_pos, y_pos, z_pos)}. Current targets: {(x_target, y_target, z_target)}."  # noqa: E501
            )
            GPIO.output(SLEEP, GPIO.LOW)

        logging.debug("End of loop.\n")


def move_x(x_pos: float, x_target: float) -> float:
    """Move along x-axis one step toward target position. If already there, do nothing."""
    if x_pos < x_target:
        GPIO.output(DIR_X, CW)
        GPIO.output(STEP_X, GPIO.HIGH)
        x_pos += INCREMENT
    if x_pos > x_target:
        GPIO.output(DIR_X, CCW)
        GPIO.output(STEP_X, GPIO.HIGH)
        x_pos -= INCREMENT
    return x_pos


def move_y(y_pos: float, y_target: float) -> float:
    """Move along y-axis one step toward target position. If already there, do nothing."""
    if y_pos < y_target:
        GPIO.output(DIR_Y, CW)
        GPIO.output(STEP_Y, GPIO.HIGH)
        y_pos += INCREMENT
    if y_pos > y_target:
        GPIO.output(DIR_Y, CCW)
        GPIO.output(STEP_Y, GPIO.HIGH)
        y_pos -= INCREMENT
    return y_pos


def move_z(z_pos: float, z_target: float) -> float:
    """Move along z-axis one step toward target position. If already there, do nothing."""
    if z_pos < z_target:
        GPIO.output(DIR_Z, CW)
        GPIO.output(STEP_Z, GPIO.HIGH)
        z_pos += INCREMENT
    if z_pos > z_target:
        GPIO.output(DIR_Z, CCW)
        GPIO.output(STEP_Z, GPIO.HIGH)
        z_pos -= INCREMENT
    return z_pos


def is_in_position(positions: Tuple[float, float, float], targets: Tuple[float, float, float]) -> bool:
    """Check if current x, y, z positions are as close to their targets as they can be.

    :param positions: Current positions
    :type positions: Tuple[float, float, float]
    :param targets: Current targets
    :type targets: Tuple[float, float, float]
    :return: True if in position, False otherwise
    :rtype: bool
    """
    return all(abs(pos - target) <= INCREMENT for pos, target in zip(positions, targets))


def setup_gpio() -> None:
    logging.info("Starting GPIO setup.")

    # Setting GPIO mode to BOARD. This uses straight up pin numbers as
    # opposed to actual GPIO channel numbers. For more info on this decision,
    # visit https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/#pin-numbering
    GPIO.setmode(GPIO.BOARD)

    # Set each axis's direction and step pins as outputs as well as the sleep pin.
    GPIO.setup(DIR_X, GPIO.OUT)
    GPIO.setup(STEP_X, GPIO.OUT)

    GPIO.setup(DIR_Y, GPIO.OUT)
    GPIO.setup(STEP_Y, GPIO.OUT)

    GPIO.setup(DIR_Z, GPIO.OUT)
    GPIO.setup(STEP_Z, GPIO.OUT)

    GPIO.setup(SLEEP, GPIO.OUT)
    logging.info("GPIO setup complete.")


def cleanup() -> None:
    """Run GPIO cleanup to return all channels to safe."""
    GPIO.cleanup()
    logging.info("GPIO cleanup complete.")
