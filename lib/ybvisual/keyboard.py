#!/usr/bin/env python

class Keyboard:
    def __init__(self):
        print "Created keyboard"
        self.key_pressed = None
    def Process(self,_type,_key):
        if(_type=="PRESS"):
            self.key_pressed = str(_key)
        if(_type=="RELEASE"):
            self.key_pressed = None   
    def isKeyPressed(self,key):
        if(str(key) == str(self.key_pressed)):
            return True;
        else:
            return False;
    def isReleased(self,robot):
        if(self.key_pressed==None):
            robot.Stop()
KEYBOARD = Keyboard()
        
        