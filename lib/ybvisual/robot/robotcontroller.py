#!/usr/bin/env python
import rospy
from lib.ybvisual.jsonparser import JSONObject
import time
from lib.ybvisual.demomanager import DemoManager
from threading import Thread

#
# We need to import the main robot script
#
from lib.ybvisual.robot.robot import Robot
    
#
# Robot controller
#
class RobotController:
    #Initialise
    def __init__(self):
        #Define the youbot object
        self.robot = Robot();
        #Demo manager
        self.demo_manager = DemoManager(self.robot)
    #Halt execution -- acts as an emergency stop
    def Halt(self):
        self.robot.EmergencyStop()
    #Handle sensor requests
    def HandleSensorRequest(self,sname,rtype):
        rospy.loginfo("Handling sensor request")        
        rospy.loginfo("For sensor: " + str(sname))
        rospy.loginfo("And request type: " + str(rtype))
        #Camera
        if(sname=="CAMERA"):
            #Check the request type
            if(rtype=="VIEW"):
                #Return camera data
                return self.robot.GetCameraData()
    #Process incoming data
    def _Process(self,code):
        print(code)
        try:
            #eval(code,locals())
            exec(code,locals())
        except Exception as e:
            print(e)
            print(code)
    def Shutdown(self):
        rospy.signal_shutdown("Done!")
