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
from lib.ybvisual.application import Application
from lib.ybvisual.robot.robotcontroller import RobotController

#
# Primary robot server class
#
class Server:
    #
    # Use a try-except to catch any errors while initialising these variables
    #
    try:
        #Used for saving/opening existing programs
        _Application = Application()
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
            Server.Shutdown() if (JSONObject.HasAttribute(data,"SHUTDOWN") == True) else None
            return ' '
        def __call__(self,data):
            return Server.ServerCmd.Run(data) if (JSONObject.IsType(data,Server.ServerCmd.ReqString) == True) else None 
    SERVERCMD = ServerCmd()
    
    #APPLICATION MANAGEMENT COMMAND
    class ApplicationCmd:
        ReqString = "APPLICATION"
        @staticmethod
        def Run(data):
            rospy.loginfo("Received APPLICATION command")
            
            #Get the json object to handle the type of the application command
            json = JSONObject(data.getData("attribute"))
            _type = json.getData("type")
            _att = json.getData("attribute")
            _val = json.getData("value")
            rospy.loginfo("Type: " + str(_type)) # type
            rospy.loginfo("Attribute: " + str(_att)) # attribute
            rospy.loginfo("Value: " + str(_val)) # value

            #Check the application command type
            if(str(_type) == "SAVE"):
                rospy.loginfo("Saving application")
                # The attribute holds the application name
                appname = str(_att)
                # The value holds the application data
                appdata = str(_val)
                # Display info for debugging
                rospy.loginfo("Application name: " + appname)
                rospy.loginfo("Application data: " + appdata)
                Server._Application.Save(appdata,appname)
            elif(str(_type) == "OPEN"):
                rospy.loginfo("Opening application")
                #Now attempt to open the application
                #Attribute holds the application name
                appname = str(_att)
                rospy.loginfo("Attempting to open application: " + str(appname))
                _app = Server._Application.Open(appname)
                _app.replace("?","")
                rospy.loginfo("Opened application: " + str(_app))
                return _app               
            elif(str(_type) == "LIST"):
                rospy.loginfo("Getting saved application list")
                _list = Server._Application.getSaved()
                print "apps: " + _list
                return _list
            
            return ' '
        def __call__(self,data):
            return Server.ApplicationCmd.Run(data) if (JSONObject.IsType(data,Server.ApplicationCmd.ReqString) == True) else None
    APPLICATIONCMD = ApplicationCmd()
    
    #PASSWORD COMMAND
    class PasswordCmd:
        ReqString = "PASSCHECK"
        @staticmethod
        def Run(data):
            rospy.loginfo("Received PASSWORD CHECK command")
            return Server._Session.checkPassword(data,web.ctx.ip)
        def __call__(self,data):
            return Server.PasswordCmd.Run(data) if (JSONObject.IsType(data,Server.PasswordCmd.ReqString) == True) else None
    PASSWORDCMD = PasswordCmd()
    #RUN COMMAND
    class RunCmd:
        ReqString = "RUN"
        @staticmethod
        def Run(data):
            rospy.loginfo("Received RUN command")
            #The robot will process the given command
            #Server.Robot.SetData(data)
            Server.Robot._Process(data.getData("attribute"))
            return ' '
        def __call__(self,data):
            return Server.RunCmd.Run(data) if (JSONObject.IsType(data,Server.RunCmd.ReqString) == True) else None
    RUNCMD = RunCmd()
    #SENSORS COMMAND
    class SensorsCmd:
        ReqString = "SENSORS"
        @staticmethod
        def Run(data):
            rospy.loginfo("Received sensors request command")
            _att = data.getData('attribute')
            _val = data.getData('value')
            result = Server.Robot.HandleSensorRequest(_att,_val)
            return result
        def __call__(self,data):
            return Server.SensorsCmd.Run(data) if (JSONObject.IsType(data,Server.SensorsCmd.ReqString) == True) else None
    SENSORSCMD = SensorsCmd()
    #Server Commands
    CMD = [SERVERCMD,APPLICATIONCMD,PASSWORDCMD,RUNCMD,SENSORSCMD]

    #The API variable handles POST messages sent to the main index page
    @staticmethod
    def CheckData(data):
        for i in range(0,len(Server.CMD)):
            ret = Server.CMD[i](data)
            if(ret!=None):
                return ret
        return ' '
            
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
        print data
        #Init given data as a JSON object
        json = JSONObject(data)
        #Check given data
        res = Server.CheckData(json)
        return res

#Set callback for ROS shutdown
rospy.on_shutdown(Server.Shutdown)

#Main method
if __name__ == "__main__":
    try:
        Server.Start()
        print "Server shutdown"
    except Exception as e:
        print "Exception found"
        print e
        
        
