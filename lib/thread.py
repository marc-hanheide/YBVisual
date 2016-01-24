#!/usr/bin/env python

import threading, time

#
# Class for starting a thread that runs a specified function
#
#class Thread(threading.Thread):    
#    #Initialise
#    def __init__(self,func):
#        super(Thread,self).__init__(target=func)
#        self._stop = threading.Event()
#    #Stop the thread
#    def Stop(self):
#        self._stop.set()
#        print "Thread stopped successfully"
#    #Was the thread stopped
#    def Stopped(self):
#        print "Thread stopped condition: " + self._stop.isSet()
#        return self._stop.isSet()
#    #Start the thread
#    def Start(self):
#        self.start()



class _Thread(threading.Thread):
    def __init__(self,function):
        Thread.__init__(self)
        self.function = function
    def run(self):
        while True:
            if(self.function!=None):
                self.function()
        
        
        