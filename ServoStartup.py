#!/usr/bin/python3

# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////

import spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
spi = spidev.SpiDev()

# For this example we will use the RPiMIB to create the PWM signals to talk to Servo motors and motor controllers.
#
# The RPiMIB (Raspberry Pi Multi Interface Board) has two PWM outputs, which will be sufficient for this example. If
# need more thanimport spidev
import os
from time import sleep
import RPi.GPIO as GPIO
from pidev.stepper import stepper
from Slush.Devices import L6470Registers
spi = spidev.SpiDev()

# Init a 200 steps per revolution stepper on Port 0
s0 = stepper(port=0, micro_steps=32, hold_current=20, run_current=20, accel_current=20, deaccel_current=20,
             steps_per_unit=200, speed=8)
# 2 PWM outputs we typically use the Adafruit 16 Channel PWM module that uses the I2C bus on the RPi.
# More info on that later - but here is a sneak peak if you are interested
# https://learn.adafruit.com/16-channel-pwm-servo-driver?view=all
#
# The RPiMIB was a hardware and software project developed in conjunction with DPEA mentors, teachers and students.
# Joe Kleeburg a mentor for the DPEA, did the electrical and mechanical design of the circuit and PCB.
# Doug Whetter has taken the lead on firmware and software development.
# The RPiMIB has a couple of very specific goals:
# 1. Expand the available I/O on the Raspberry Pi, while the RPi is connected to a Slush engine which uses 99% of the
# built in RPi I/O
# 2. Enable the RPi to connect to 5V SPI and I2c buses (versus its native 3.3V SPI and I2c buses)
# 3. Provide battery backed up power to the RPi in the event of power loss, and gracefully shutdown the RPi.
#
# The above functionality if the RPiMIB is made possible primarily by the use of a Cypress Programmable System On a Chip
# (PSOC) which is basically a highly sophisticated programmable chip on the RPiMIB. This Chip has to be programmed with
# Firmware - then that firmware can be accessed by software written on the RPi. The Firmware is written in a combination
# of C++ and a proprietary hardware design language / user interface.
#
# The schematics and documentation for the RPiMIB is on github - search for the RPiMIB repo.
#
# So for a RPiMIB to work several things have to happen:
# 1. The board needs to be assembled correctly - we have DPEA electrical students working on these
# 2. The Cypress PSOC needs to have the correct firmware programmed on it - you can verify the firmware version from the
#    python library and print it to the screen, so you always know which version of the firmware you are using
# 3. The RPiMIB needs to be correctly assembled and plugged in to the RPi, Slush Engine and associated power supplies
# 4. The Software library needs to be correctly installed and kept up to date with updates. Fortunately the software
#    resides in RaspberryPiCommon Github repo which is something you should always keep up to date.
#
# As mentioned, the Software library is in RaspberryPiCommon/pidev/Cyprus_Commands/Cyprus_Commands.py
# The code is readable - and there is a very well written README.md with example usage in the same folder as the library.
#
# The PWM Ports on the RPiMIB are P4 and P5. The software library can be used to control both servo motors and motor
# controllers like the Talon that use a servo motor input and convert that to a high current drive that can control
# large motors.
#
# In addition to creating PWM that is used to control servo motors and servo motor style motor controllers the software
# library has been designed to also create non servo specific PWM for controlling industry standard motor controllers.
# Basically the Servo PWM is a special case of industry standard PWM, hopefully we will get to more on this later.
#

# To get a RC servo motor signal out of P4 of the RPiMIB do the following:
cyprus.initialize()  # initialize the RPiMIB and establish communication
cyprus.setup_servo(1)  # sets up P4 on the RPiMIB as a RC servo style output
cyprus.set_servo_position(1, 0)  # 1 specifies port P4, 0 is a float from 0-1 that specifies servo position ~(0-180deg)
sleep(1) # wait one second for the servo to get there... minimum here should be about sleep(0.05)
cyprus.set_servo_position(1, .5)  # 1 specifies port P4, 0.5 specifies servo position ~(0-180deg) range of (0-1)
# when done disconnect the RPiMIB communication
cyprus.close()

# To get a RC servo motor CONTROLLER signal out of P5 of the RPiMIB do the following:
cyprus.initialize()  # initialize the RPiMIB and establish communication
cyprus.setup_servo(2)  # sets up P5 on the RPiMIB as a RC servo motor controller style output
# for loop will set speed all the way from 0-full reverse to 0.5-halt to 1-full forward then halt with half second delays
for i in range(5, 10, 1):
    cyprus.set_servo_position(2, i/10.0)  # 2 specifies port P5, i is a float that specifies speed
    sleep(0.5)
cyprus.set_servo_position(1, 0.5)  # halt the motor
cyprus.close()  # when done disconnect the RPiMIB communication

# To get a Industrial PWM output on P5 to control something like a Cytron Motor Controller do the following:
cyprus.initialize()  # initialize the RPiMIB and establish communication
# the following command will set up port 2 (P5) to put out a 100000HZ (100KHz) signal with a 50% high time or duty cycle
cyprus.set_pwm_values(2, period_value=100000, compare_value=50000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
# Motor controller Ex. Cytron MD10C connected to P5, the connected motor would be running ~50% max rpm
cyprus.set_pwm_values(2, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL) #  Motor OFF
cyprus.close()

# To get sensors and other I/O to work with RPiMIB
# The RPiMIB has four multipurpose I/O ports. Ports P6, P7, P8 and P9
#
# The command to read is cyprus.read_gpio() which will return 4 bits which represents ALL GPIO pins (P6-P9)
# To get the actual value of a particular port one needs to do a bitwise AND as per example below

from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus

cyprus.initialize()
if (cyprus.read_gpio() & 0b0001):    # binary bitwise AND of the value returned from read.gpio()
    print("GPIO on port P6 is HIGH")
elif (cyprus.read_gpio() & 0b0010):
    print("GPIO on port P7 is HIGH")
elif (cyprus.read_gpio() & 0b0100):
    print("GPIO on port P8 is HIGH")
else (cyprus.read_gpio() & 0b1000):
    print("GPIO on port P9 is HIGH")
cyprus.close()

# To get the status of a GPIO pin one could create a method like this:
#     def isGPIO_P6_HIGH(self):
#         return (cyprus.read_gpio() & 0b0001) == 1
#
# Checks to see if gpio read and bitwise AND are equal to 1. If so returns TRUE otherwise returns FALSE


# Exercises:
# 1. Connect a servo motor to P4 and make it go from 0 degrees to 180 degrees as two binary states.
# 1a. Connect a limit switch to P6 and make servo on P4 be at 0deg when limit switch is pressed (closed) and 180deg when open
# 2. Connect a Talon motor controller to P4. Turn on a DC motor at full speed clockwise. Stop 5 seconds then Full speed counterclockwise
# 2a. Make DC motor connected to Talon ramp up from 0rpm to full speed over 20 seconds in equal intervals.
# 2b. Connect a limit switch to P6 and make DC motor connected to talon on P4 be at full speed clockwise when limit switch is pressed (closed) and stopped when open
# 3. Connect a Cytron motor controller and a dc motor to P5. Turn on a DC motor at full speed clockwise. Stop 5 seconds then Full speed counterclockwise
# 3a. Connect a proximity sensor to P7 and make the cytron motor controller on P5 be at full speed clockwise when the proximity sensor is detecting metal and stopped when it is not detecting metal