#!/usr/bin/env python
import rospy

from lib.ybvisual.robot.sensors.camera import Camera



class RobotSensors:
    #   
    # Container class for robotic sensors
    #   
    class SensorContainer:
        #Initialise
        def __init__(self):
            #Arraylist holds currently available sensors
            self.container = []
            rospy.loginfo("Initialised sensor container")
        #Check if the container already contains a sensor of this type            
        def HasType(self,_type):
            for i in range(0,len(self.container)):
                if str(_type)==self.container[0]:
                    rospy.loginfo("Robot has sensor of type: " + str(_type))
                    return True
            rospy.loginfo("Robot does not have sensor of type: " + str(_type))
            return False
        #Replace a sensor type            
        def ReplaceType(self,_type,_class):
            if (_type!=None) and (_class!=None):
                for i in range(0,len(self.container)):
                    if str(_type)==self.container[0]:
                        rospy.loginfo("Replaced sensor type: " + str(_type))
                        self.container[i] = [_type,_class]
                #If not found - just add new
                self.AddType(_type,_class)
        #Add a sensor type, with its appropriate class
        def AddType(self,_type,_class):
            #Only attempt to add if a sensor of this type does not already exist
            if (self.HasType(_type)==False) and (_type!=None) and (_class!=None):
                rospy.loginfo("Added sensor type: " + str(_type))
                self.container.append([_type,_class])
        #Remove a sensors type
        def RemoveType(self,_type):
            for i in range(0,len(self.container)):
                cur = self.container[i]
                name = cur[0]
                if name!=None and name==str(_type):
                    rospy.loginfo("Removed sensor type: " + str(_type))
                    self.container.pop(i)
        #Get sensor of type
        def GetType(self,_type):
            s = None
            for i in range(0,len(self.container)):
                cur = self.container[i]
                name = cur[0]
                if name!=None and name==str(_type):
                    rospy.loginfo("Getting sensor of type: " + str(_type))
                    s = cur[1]
            if(s==None):
                rospy.loginfo("Couldn't find sensor of type: " + str(_type) + " , returning NULL")
            return s
    
    #Initialise
    def __init__(self):
        #Sensor container
        self.sensors = RobotSensors.SensorContainer()
        rospy.loginfo("Initialised robot sensors object")
    #Is the robot using a camera sensor
    def UsingCamera(self):
        if self.sensors != None:
            rospy.loginfo("Checking if robot has camera")
            return self.sensors.HasType("camera")
    #Add a new camera sensor - if there one that exists, it will be replaced
    def AddCamera(self):
        if self.sensors != None:
            rospy.loginfo("Adding camera sensor to robot")
            self.sensors.ReplaceType("camera",Camera(False))
    #Get the robots camera sensor
    def GetCamera(self):
        if self.sensors != None:
            rospy.loginfo("Getting the robots camera sensor")
            return self.sensors.GetType("camera")
            
        
                
                
                
        

