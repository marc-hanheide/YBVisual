#!/usr/bin/env python

import web
import sys
from lib.jsonparser import *
from lib.session import *
from lib.robot import *
from lib.tmux import *
from lib.keyboard import *
from lib.console import ServerConsole
render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/console','console'
)

#Holds session information
session = Session()
#Used for saving/opening existing programs
program = Program()
#Robot controller - Processes robot specific commands
robot = RobotController()
#Web application
app = web.application(urls,globals())


#Create the ros shutdown event
def onShutdown():
    print "Ros shutdown detected, shutting down server."
    app.stop()
    robot.Shutdown()
rospy.on_shutdown(onShutdown)

#console page
class console:
    def GET(self):
        return render.console()
    def POST(self):
        #Data will contain the text entered into the console window
        data =  web.data()
        print "Received Data: " + data
        #The received data should be json
        json = JSONObject(data);
        #The type will contain the given command
        _type = json.getData('type')
        
        #
        # AUTH CHECK
        #        
        if(_type=="PASSCHECK"):
            return session.checkAdminPassword(json)
        
        
        #
        # COMMAND CHECKS
        #
        #CONNECTIONS
        if(_type=="CONNECTIONS"):
            return session.getConnections();
        #REJECT
        if(_type=='REJECT'):
            #The attribute is the user ip..
            session.removeConnection(str(json.getData('attribute')))
        
        #REJECTALL
        if(_type=="REJECTALL"):
            session.clearConnections();

        return ""



#main index page
class index:
    def GET(self):
        return render.index()
    def POST(self):
        data = web.data()
        #print "Received Data: " + data
        #Create JSON object using given data - if required
        json = JSONObject(data);
        _type = json.getData('type')
        _att = json.getData('attribute');
        _val = json.getData('value');
        #print "Received JSON data with type: " + _type
        #Sever control commands
        if(_type == "SERVER"):
            #Was this a shutdown request?
            if(_att == "SHUTDOWN"):
                #Shutdown the server
                print "Attempting to shutdown the server.."
                onShutdown()
        #
        # Check if received data is an auth check
        #
        if(_type == 'AUTHCHECK'):
            return session.isAuth(web.ctx.ip)    
        #
        # Check if this is a password check
        #
        elif(_type == 'PASSCHECK'):
            return session.checkPassword(json,web.ctx.ip)
        #
        # Check if SAVE data was given
        #
        elif(_type == "APPSAVE"):
            #Save the program using the given data
            program.Save(json);
        #
        # Check if OPEN data was given
        #
        elif(_type == "APPOPEN"):
            #Open program using given program name
            #We need to get the application name
            _name = json.getData('attribute');
        #
        # User requests list of saved applications
        #
        elif(_type == "APPLIST"):
            #We need return a JSON object containing a list of saved applications
            return program.getSaved()
        #
        # Emergency stop
        #
        elif(_type =="ESTOP"):
            print "Halt key pressed"
            #Ensure robot is stopped when e-stop is called
            robot.Halt()
        #
        # Else we can process robot specific commands
        #
        elif(_type =="RUN"):
            #Process given command
            robot.SetData(json)

if __name__ == "__main__":
    app.run()
    print "Server shutdown"
    #Find server process - and kill it
    os.system("pkill -1 -f server.py")
                         
