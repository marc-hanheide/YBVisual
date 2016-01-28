#!/usr/bin/env python
import os
import tmuxp

#
# TMUX sessions manager
#
class TMUXManager:
    Server = None
    #
    # Initialise
    #
    def __init__(self):
        TMUXManager.Server = tmuxp.Server()
        #Ensure that there are no currently running sessions
        TMUXManager.Server.kill_server()
        #self.server
    #
    # Creates a session from config file
    #
    def Load(self,cfg):
        os.system("tmuxp load " + cfg)
    @staticmethod
    def Shutdown():
        print "Shutting down tmux server"
        TMUXManager.Server.kill_server()
