"""Movement controller"""

__all__ = ["run", "cleanup"]

import logging
from time import sleep

import RPi.GPIO as GPIO

import data

INCREMENT = 5.08 / 400  # Lead screw pitch / steps per rev

CW = 1  # clockwise rotation
CCW = 0  # counterclockwise rotation

STEP_X = 21  # x-axis step GPIO pin
DIR_X = 22  # x-axis direction GPIO pin

STEP_Y = 10  # y-axis step GPIO pin
DIR_Y = 12  # y-axis direction GPIO pin

STEP_Z = 3  # z-axis step GPIO pin
DIR_Z = 5  # z-axis direction GPIO pin

STEP_A = 11  # a-axis step GPIO pin
DIR_A = 13  # a-axis direction GPIO pin

STEP_B = 38  # b-axis step GPIO pin
DIR_B = 40  # b-axis direction GPIO pin

SLEEP = 15  # sleep GPIO pin


def run() -> None:
    """Receive movement instructions and execute until stopped."""
    setup_gpio()

    x_pos = y_pos = z_pos = a_pos = b_pos = 0.0

    logging.info("Infinite loop starting.")
    while True:
        x_target = data.targets["x"]
        y_target = data.targets["y"]
        z_target = data.targets["z"]
        a_target = data.targets["a"]
        b_target = data.targets["b"]

        logging.debug(f"Targets: {data.targets}.")

        if not is_in_position(x_pos, y_pos, z_pos, a_pos, b_pos, x_target, y_target, z_target, a_target, b_target):
            GPIO.output(SLEEP, GPIO.HIGH)

            x_pos = move_x(x_pos, x_target)
            y_pos = move_y(y_pos, y_target)
            z_pos = move_z(z_pos, z_target)
            a_pos = move_a(a_pos, a_target)
            b_pos = move_b(b_pos, b_target)

            sleep(0.00125)

            GPIO.output(STEP_X, GPIO.LOW)
            GPIO.output(STEP_Y, GPIO.LOW)
            GPIO.output(STEP_Z, GPIO.LOW)
            GPIO.output(STEP_A, GPIO.LOW)
            GPIO.output(STEP_B, GPIO.LOW)
        else:
            GPIO.output(SLEEP, GPIO.LOW)

        logging.debug("End of loop.\n")


def move_x(x_pos: float, x_target: float) -> float:
    """Move along x-axis one step toward target position. If already there, do nothing."""
    if compare(x_pos, x_target):
        return x_pos
    if x_pos < x_target:
        GPIO.output(DIR_X, CW)
        GPIO.output(STEP_X, GPIO.HIGH)
        x_pos += INCREMENT
        logging.debug(f"Moved X-axis CW (+). Now {x_pos}.")
    elif x_pos > x_target:
        GPIO.output(DIR_X, CCW)
        GPIO.output(STEP_X, GPIO.HIGH)
        x_pos -= INCREMENT
        logging.debug(f"Moved X-axis CCW (-). Now {x_pos}.")
    return x_pos


def move_y(y_pos: float, y_target: float) -> float:
    """Move along y-axis one step toward target position. If already there, do nothing."""
    if compare(y_pos, y_target):
        return y_pos
    if y_pos < y_target:
        GPIO.output(DIR_Y, CW)
        GPIO.output(STEP_Y, GPIO.HIGH)
        y_pos += INCREMENT
        logging.debug(f"Moved Y-axis CW (+). Now {y_pos}.")
    elif y_pos > y_target:
        GPIO.output(DIR_Y, CCW)
        GPIO.output(STEP_Y, GPIO.HIGH)
        y_pos -= INCREMENT
        logging.debug(f"Moved Y-axis CCW (-). Now {y_pos}.")
    return y_pos


def move_z(z_pos: float, z_target: float) -> float:
    """Move along z-axis one step toward target position. If already there, do nothing."""
    if compare(z_pos, z_target):
        return z_pos
    if z_pos < z_target:
        GPIO.output(DIR_Z, CW)
        GPIO.output(STEP_Z, GPIO.HIGH)
        z_pos += INCREMENT
        logging.debug(f"Moved Z-axis CW (+). Now {z_pos}.")
    elif z_pos > z_target:
        GPIO.output(DIR_Z, CCW)
        GPIO.output(STEP_Z, GPIO.HIGH)
        z_pos -= INCREMENT
        logging.debug(f"Moved Z-axis CCW (-). Now {z_pos}.")
    return z_pos


def move_a(a_pos: float, a_target: float) -> float:
    """Move along a-axis one step toward target position. If already there, do nothing."""
    if compare(a_pos, a_target):
        return a_pos
    if a_pos < a_target:
        GPIO.output(DIR_A, CW)
        GPIO.output(STEP_A, GPIO.HIGH)
        a_pos += INCREMENT
        logging.debug(f"Moved A-axis CW (+). Now {a_pos}.")
    elif a_pos > a_target:
        GPIO.output(DIR_A, CCW)
        GPIO.output(STEP_A, GPIO.HIGH)
        a_pos -= INCREMENT
        logging.debug(f"Moved A-axis CCW (-). Now {a_pos}.")
    return a_pos


def move_b(b_pos: float, b_target: float) -> float:
    """Move along b-axis one step toward target position. If already there, do nothing."""
    if compare(b_pos, b_target):
        return b_pos
    if b_pos < b_target:
        GPIO.output(DIR_B, CW)
        GPIO.output(STEP_B, GPIO.HIGH)
        b_pos += INCREMENT
        logging.debug(f"Moved B-axis CW (+). Now {b_pos}.")
    elif b_pos > b_target:
        GPIO.output(DIR_B, CCW)
        GPIO.output(STEP_B, GPIO.HIGH)
        b_pos -= INCREMENT
        logging.debug(f"Moved B-axis CCW (-). Now {b_pos}.")
    return b_pos


def is_in_position(
    x_pos: float,
    y_pos: float,
    z_pos: float,
    a_pos: float,
    b_pos: float,
    x_target: float,
    y_target: float,
    z_target: float,
    a_target: float,
    b_target: float,
) -> bool:
    """Check if current x, y, z, a, b positions are as close to their targets as they can be."""

    x_cmp = compare(x_pos, x_target)
    y_cmp = compare(y_pos, y_target)
    z_cmp = compare(z_pos, z_target)
    a_cmp = compare(a_pos, b_target)
    b_cmp = compare(b_pos, b_target)

    in_position = all((x_cmp, y_cmp, z_cmp, a_cmp, b_cmp))

    logging.debug(
        f"In position: {in_position}. X-axis: {x_cmp}. Y-axis: {y_cmp}. Z-axis: {z_cmp}. A-axis: {a_cmp}. B-axis: {b_cmp}."  # noqa: E501
    )
    logging.debug(
        f"X-axis: {x_pos, x_target}. Y-axis: {y_pos, y_target}. Z-axis: {z_pos, z_target}. A-axis: {a_pos, a_target}. B-axis: {b_pos, b_target}."  # noqa: E501
    )

    return in_position


def compare(position: float, target: float) -> bool:
    return abs(position - target) <= INCREMENT / 2


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

    GPIO.setup(STEP_A, GPIO.OUT)
    GPIO.setup(DIR_A, GPIO.OUT)

    GPIO.setup(STEP_B, GPIO.OUT)
    GPIO.setup(DIR_B, GPIO.OUT)

    GPIO.setup(SLEEP, GPIO.OUT)
    logging.info("GPIO setup complete.")


def cleanup() -> None:
    """Run GPIO cleanup to return all channels to safe."""
    GPIO.cleanup()
    logging.info("GPIO cleanup complete.")
