#!/usr/bin/env python

#
# Standard import
#
import web
import sys
import rospy
import os

#
# Robot lib imports
#
from lib.ybvisual.jsonparser import JSONObject
from lib.ybvisual.session import Session
from lib.ybvisual.program import Program
from lib.ybvisual.robot.robotcontroller import RobotController

#
# Primary robot server class
#
class Server:
    #
    # Use a try-except to catch any errors while initialising these variables
    #
    try:
        #Holds session information
        _Session = Session()
        #Used for saving/opening existing programs
        _Program = Program()
        #Robot controller - Processes robot specific commands
        Robot = RobotController()    
        #Define templates folder
        Templates = web.template.render("templates/")
        #Define urls
        Urls = ('/','index')
        #Server app    
        App = web.application(Urls,globals())
    except Exception as e:
        print "Found error, killing process.."
        print e
        os.system("pkill -1 -f server.py")
        
    
    #Start the server
    @staticmethod
    def Start():
        Server.App.run()
    
    #Function is used to stop the server
    @staticmethod
    def Shutdown():
        print "Ros shutdown detected, shutting down server."
        Server.App.stop()
        #Also shutdown the robot
        Server.Robot.Shutdown()
    
    #
    #Define command options for the server API as classes
    #These include the functions called by the command
    #And the required String
    #SERVER COMMAND    
    class ServerCmd:
        ReqString = "SERVER"
        @staticmethod
        def Run(data):
            rospy.loginfo("Received SERVER command")
            #Is this a shutdown request
            Server.Shutdown() if (JSONObject.HasAttribute(data) == True) else None
        def __call__(self,data):
            Server.SeverCmd.Run(data) if (JSONObject.IsType(data,Server.ServerCmd.ReqString) == True) else None 
    SERVERCMD = ServerCmd()
    
    #PASSWORD COMMAND
    class PasswordCmd:
        ReqString = "PASSCHECK"
        @staticmethod
        def Run(data):
            rospy.loginfo("Received PASSWORD CHECK command")
            return Server._Session.checkPassword(data,web.ctx.ip)
        def __call__(self,data):
            Server.PasswordCmd.Run(data) if (JSONObject.IsType(data,Server.PasswordCmd.ReqString) == True) else None
    PASSWORDCMD = PasswordCmd()
    #RUN COMMAND
    class RunCmd:
        ReqString = "RUN"
        @staticmethod
        def Run(data):
            rospy.loginfo("Received RUN command")
            #The robot will process the given command
            Server.Robot.SetData(data)
        def __call__(self,data):
            Server.RunCmd.Run(data) if (JSONObject.IsType(data,Server.RunCmd.ReqString) == True) else None
    RUNCMD = RunCmd()
    
            

    #The API variable handles POST messages sent to the main index page
    @staticmethod
    def CheckData(data):
        #Server command
        Server.SERVERCMD(data)
        #Password command
        Server.PASSWORDCMD(data)
        #Run command
        Server.RUNCMD(data)
            
#
# Index page structure
#
class index:
    def GET(self):
        #Return page contents
        return Server.Templates.index()
    def POST(self):
        #Get received data
        data = web.data()
        #Init given data as a JSON object
        json = JSONObject(data)
        #Check given data
        Server.CheckData(json)

#Set callback for ROS shutdown
rospy.on_shutdown(Server.Shutdown)

#Main method
if __name__ == "__main__":
    try:
        Server.Start()
        print "Server shutdown"
        #Find server process - and kill it
        os.system("pkill -1 -f server.py")
    except Exception as e:
        print "Exception found"
        print e
        os.system("pkill -1 -f server.py")
        
        