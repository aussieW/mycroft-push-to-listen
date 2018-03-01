from mycroft.util.log import getLogger
from mycroft.skills.core import MycroftSkill
import subprocess
#from os.path import join, abspath, dirname

__author__ = 'aussieW'

LOGGER = getLogger(__name__)

class MycroftPushToListen(MycroftSkill):
    def __init__(self):
        super(MycroftPushToListen, self).__init__(name='MycroftPushToListen')
        buttonPin = self.settings['gpio']
        
    def initialize(self):
        # start the button listener
        #subprocess.call(join(abspath(dirname(__file__)), 'button.py'))
        proc = subprocess.Popen(['python', '/opt/mycroft/skills/mycroft-push-to-listen/button.py', buttonPin])
        
    def shutdown(self):
        # shutdown the button.py process
        proc.kill()
        super(MycroftPushToListen, self).shutdown()
        
def create_skill():
    return MycroftPushToListen()
