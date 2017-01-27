#!/usr/bin/env python
import rospy
import os

#
# Local console may be used for changing, and requesting basic information locally on the robot
#
class LocalConsole:
    #Initialise
    def __init__(self):
        self.EXIT_REQUESTED = False
        self.Start()
    
    #
    # Start the console interface
    #
    def Start(self):
        #Loop until exit is requested
        while self.EXIT_REQUESTED == False:
            #Get user input and check for commands
            _input = raw_input("(CONSOLE - Type 'help' for a list of available commands) Enter Command: ")
            #Help requested
            if (_input=='help'):
                self.Help()
            #Password change requested
            elif(_input=='password'):
                self.Password()
            #Shutdown requested
            elif(_input=="shutdown"):
                self.Shutdown()
    #
    # Help requested
    #
    def Help(self):
        print 'Commands list: '
        print 'Help - View available commands'
        print 'password - Change system password'
        print "shutdown - Shutdown the server"

    #
    # Password change requested
    #
    def Password(self):
        _pass = raw_input ("Enter new system password: ")
    #
    # Server shutdown
    #
    def Shutdown(self):
        print "Server shutdown"
        rospy.signal_shutdown("Done!")
        #Find server process - and kill it
        os.system("pkill -1 -f server.py")

if __name__ == "__main__":
    console = LocalConsole()
    console.Start()
