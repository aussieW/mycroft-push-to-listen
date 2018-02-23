# Mycroft quick and dirty led and button tester
#
# Put mbus.py, button.py and light.py in /home/pi
# Run python lights.py in another terminal
# or better: add it to your autorun.sh like this:
# python /home/pi/lights.py </dev/null &>/dev/null &
# just before:
# else
#   # running from a SSH session
#   echo "Remote session"
# fi
#
# Todo: make proper daemon
# quit using crtl + \
#
# short press does a stop, longer then 2 seconds presses start mic listening

###import subprocess
import time
import RPi.GPIO as GPIO
from subprocess import call

gpio_pin=14 # The GPIO pin the button is attached to
longpress_threshold=1 # If button is held this length of time, tells system to leave light on
pressed_time = 0  # The time the button was last pressed
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set the mode of the button

try:
    # Loop around waiting for a callback to occur
    while True:
        
        print 'Wait for a button press'
 #       print GPIO.input(gpio_pin)
	GPIO.wait_for_edge(gpio_pin, GPIO.FALLING, bouncetime=10)  # wait for button to trigger
#        print 'detected a button push at ' + time.strftime('%\%m\%d %H:%m:%s')
        print GPIO.input(gpio_pin)
        # Wait for the button to settle.
        time.sleep(.03)
        # Set up a timer to see how long the button was pushed for.
        pressed_time = time.time()
        # Add an event listener for the release of the button.
        #GPIO.add_event_detect(SwitchExternalAmp, GPIO.RISING)
		
        while (GPIO.input(gpio_pin) == 1):  # and (time.time() - pressed_time < longpress_threshold):
            # Loop until button is released.
#            print 'button held'
            time.sleep(0.01)
#        print 'botton released'
        if time.time() - pressed_time < longpress_threshold:
            call(['python', "./scripts/mbus.py", "localhost", "mycroft.mic.listen"])
        else:
            call(['python', "./scripts/mbus.py", "localhost", "mycroft.stop"])
        time.sleep(1)
		
except KeyboardInterrupt:
    # Clean up interrupts prior to exiting.
    print 'cleaning up GPIOs ...'
    GPIO.cleanup()
    print '... exiting'
