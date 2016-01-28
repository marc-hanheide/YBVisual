#!/usr/bin/env python
from threading import Thread
import sys

#Console class
class ServerConsole:
    #Initialise
    def __init__(self,app):
        print "Initialising console"
        self.running = True
        self.thread = Thread(target=self._Func,args = ())
        self.thread_is_running = True
        self.app = app
    #Is the console running?
    def isRunning(self):
        return self.running
    #Thread function
    def _Func(self):
        while self.thread_is_running:
            #While is running
            while self.isRunning():
                    #Wait for next input
                    i = str(raw_input("enter command: "))
                    print "Console command entered: " + i
                    if(i=="shutdown"):
                        "Shutdown request"
                        self.app.stop()
    #Start the console
    def Start(self):
        print "Starting console"
        self.thread.start()
        self.running = True
    #Stop the console
    def Stop(self):
        print "Stopping console"
        self.running = False
        self.thread_is_running = False
