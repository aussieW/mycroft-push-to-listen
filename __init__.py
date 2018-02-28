from mycroft.util.log import getLogger
from mycroft.skills.core import MycroftSkill
import subprocess
from os.path import join, abspath, dirname

__author__ = 'aussieW'

LOGGER = getLogger(__name__)

class MycroftPushToListen(MycroftSkill):
    def __init__(self):
        super(MycroftPushToListen, self).__init__(name='MycroftPushToListen')
        
    def initialize(self):
        # start the button listener
        subprocess.call(join(abspath(dirname(__file__)), 'button.py'))
        
def create_skill():
    return MycroftPushToListen()
