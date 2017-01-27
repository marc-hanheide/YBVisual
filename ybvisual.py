#!/usr/bin/env python

# ---------------------------
# Defines the main executable file
# ---------------------------


#!/usr/bin/env python

#Import ybvisual tmux lib
from lib.ybvisual.tmux import *
import sys
import argparse
import time

#
# Define command line args
#
try:
    parser = argparse.ArgumentParser(description="YBVisual launcher")
    parser.add_argument('using_sim',metavar='S',type=int,help='1 if using sim, else 0 if using real ROS drivers')
except Exception as e:
    print "Error while creating arg parser"
    print e


#Program entry
if __name__ == "__main__":
    #Check for errors
    try:
        #Will this be run using gazebo?
        using_gazebo = "0"
        #Manager variable
        manager = TMUXManager()
        #Load def
        #
        # Check given args.. will this be running on the real drivers, or simulation?
        #
        _args = parser.parse_args()
        using_gazebo = str(vars(_args)['using_sim'])
        
        #Check if gazebo should be used, and load the appropriate yaml file
        if using_gazebo == "0":
            manager.Load("lib/tmux_def/rsession.yaml") #Use ROS drivers (run on real robot)
        elif using_gazebo == "1":
            manager.Load("lib/tmux_def/rsession_gazebo.yaml") #Use gazebo
        else:
            print "Invalid args"
    #Exception thrown
    except Exception as e:
        print "Unable to load tmux session, exception thrown"
        print e

