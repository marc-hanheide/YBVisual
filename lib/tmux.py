#!/usr/bin/env python
import os
import tmuxp

#
# TMUX sessions manager
#
class TMUXManager:
    #
    # Initialise
    #
    def __init__(self):
        self.server = tmuxp.Server()
        #Ensure that there are no currently running sessions
        self.server.kill_server()
        self.server
    #
    # Creates a session from config file
    #
    def Load(self,cfg):
        os.system("tmuxp load " + cfg)