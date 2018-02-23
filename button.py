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
longpress_threshold=2 # If button is held this length of time, tells system to leave light on
pressed_time = 0  # The time the button was last pressed
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set the mode of the button

#GPIO.add_event_detect(gpio_pin, GPIO.FALLING, callback=buttonPressed, bouncetime=200)
#GPIO.add_event_detect(gpio_pin, GPIO.RISING, callback=buttonReleased)

def buttonPressed(channel):
    global pressed_time, longpress_threshold
#    print "Button changed..."
    if GPIO.input(gpio_pin) == True:
#        print 'pressed'
        pressed_time=time.time()
    else:
#        print 'released'
        print time.time() - pressed_time, time.time() - pressed_time < longpress_threshold
        if time.time() - pressed_time < longpress_threshold:
#            print 'listen'
            #call(['python', "/home/pi/mbus.py", "localhost", "mycroft.mic.listen"])
	    call(['python', "./scripts/mbus.py", "localhost", "mycroft.mic.listen"])
        else:
#            print 'stop'
            #call(['python', "/home/pi/mbus.py", "localhost", "mycroft.stop"])
	    call(['python', "./scripts/mbus.py", "localhost", "mycroft.stop"])
        # Disable the event for a couple of seconds to prevent multiple triggers.
        GPIO.remove_event_detect(gpio_pin)
        time.sleep(2)
        GPIO.add_event_detect(gpio_pin, GPIO.BOTH, callback=buttonPressed, bouncetime=20)    

GPIO.add_event_detect(gpio_pin, GPIO.BOTH, callback=buttonPressed, bouncetime=20)
#GPIO.add_event_detect(gpio_pin, GPIO.RISING, callback=buttonReleased)

try:
    # Loop around waiting for a callback to occur
    while True:
        #pass
        time.sleep(10) 		
except KeyboardInterrupt:
    # Clean up interrupts prior to exiting.
    print 'cleaning up GPIOs ...'
    GPIO.cleanup()
    print '... exiting'
