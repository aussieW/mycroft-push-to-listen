#!/usr/local/bin/python

# short press activates Mycroft to listen
# holding for more than 1 second sends a stop signal

import sys
import time
import RPi.GPIO as GPIO
from subprocess import call

gpio_pin=int(sys.argv[1])  # which GPIO the button is attached to
longpress_threshold=1  # differentiate between a short and lon press
pressed_time = 0  # The time the button was last pressed
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set the mode of the button

try:
    # Loop around waiting for a callback to occur
    while True:
        print('Wait for a button press')
        GPIO.wait_for_edge(gpio_pin, GPIO.RISING, bouncetime=500)  # wait for button to trigger
        GPIO.remove_event_detect(gpio_pin)
        print(GPIO.input(gpio_pin))
        # Set up a timer to see how long the button was held down for.
        pressed_time = time.time()
        while (GPIO.input(gpio_pin) == 1):
            # Loop until button is released.
            time.sleep(0.001)
		
        if time.time() - pressed_time < longpress_threshold:
            call(['python', "/opt/mycroft/skills/mycroft-push-to-listen/scripts/mbus.py", "localhost", "mycroft.mic.listen"])
        else:
            call(['python', "/opt/mycroft/skills/mycroft-push-to-listen/scripts/mbus.py", "localhost", "mycroft.stop"])

		
except KeyboardInterrupt:
    # Clean up interrupts prior to exiting.
    print('cleaning up GPIOs ...')
    GPIO.cleanup()
    print('... exiting')
