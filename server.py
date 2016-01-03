#!/usr/bin/env python

import web
import sys
from lib.jsonparser import *
from lib.session import *
from lib.robot import *
from lib.tmux import *
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
        if(_type=="REJECT"):
            session.clearConnections();

                
        
        return ""



#main index page
class index:
    def GET(self):
        return render.index()
        
    
    def POST(self):
        data = web.data()
        print "Received Data: " + data
        #Create JSON object using given data - if required
        json = JSONObject(data);
        _type = json.getData('type')
        print "Received JSON data with type: " + _type
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
        # Else we can process robot specific commands
        #
        elif(_type=="RUN"):
            #Process given command
            robot.Process(json)

        
      

if __name__ == "__main__":
    #We need to check if the console is being requested
    args = []
    args = sys.argv
    app = web.application(urls,globals())
    app.run()
        