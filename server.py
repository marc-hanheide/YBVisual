#!/usr/bin/env python

import web
from lib.jsonparser import *
from lib.session import *
from lib.robot import *
from lib.tmux import *
render = web.template.render('templates/')

urls = (
    '/', 'index'
)

#Holds session information
session = Session()
#Used for saving/opening existing programs
program = Program()
#Robot controller - Processes robot specific commands
robot = RobotController()


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
    tmuxsession = TMUXSession("lib/tsession.yaml")    
    
    app = web.application(urls,globals())
    app.run()