#!/usr/bin/env python

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
    #
    # Help requested
    #
    def Help(self):
        print 'Commands list: '
        print 'Help - View available commands'
        print 'password - Change system password'
    #
    # Password change requested
    #
    def Password(self):
        _pass = raw_input ("Enter new system password: ")

if __name__ == "__main__":
    console = LocalConsole()
    console.Start()