from time import sleep

import RPi.GPIO as GPIO

delay = 0.005  # Pause between loops
Xpos = 0
Ypos = 0
Zpos = 0
X = None
Y = None
Z = None
sleepvar = 0
sleeptarget = 3  # Number of axes
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
SLEEP = 23  # Sleep GPOI Pin


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


while sleepvar != sleeptarget:

    sleepvar = 0
    GPIO.output(SLEEP, GPIO.HIGH)

    # X Axis
    if X > Xpos:
        GPIO.output(STEP_X, GPIO.HIGH)
        GPIO.output(DIR_X, CW)
        Xpos = Xpos + 1
    if X < Xpos:
        GPIO.output(STEP_Y, GPIO.HIGH)
        GPIO.output(DIR_X, CCW)
        Xpos = Xpos - 1
    if X == Xpos:
        sleepvar = sleepvar + 1

    # Y Axis
    if Y > Ypos:
        GPIO.output(STEP_Y, GPIO.HIGH)
        GPIO.output(DIR_Y, CW)
        Xpos = Xpos + 1
    if Y < Ypos:
        GPIO.output(STEP_Y, GPIO.HIGH)
        GPIO.output(DIR_Y, CCW)
        Xpos = Xpos - 1
    if Y == Ypos:
        sleepvar = sleepvar + 1

    # Z Axis
    if Z > Zpos:
        GPIO.output(STEP_Z, GPIO.HIGH)
        GPIO.output(DIR_Z, CW)
        Xpos = Xpos + 1
    if Z < Zpos:
        GPIO.output(STEP_Z, GPIO.HIGH)
        GPIO.output(DIR_Z, CCW)
        Xpos = Xpos - 1
    if Z == Zpos:
        sleepvar = sleepvar + 1

    sleep(delay)

    GPIO.output(STEP_X, GPIO.LOW)
    GPIO.output(STEP_Y, GPIO.LOW)
    GPIO.output(STEP_Z, GPIO.LOW)


# Sleep Logic
GPIO.output(SLEEP, GPIO.LOW)
sleepvar = 0
