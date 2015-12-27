#!/usr/bin/env python

from XMLParser import *
import os
import json

#
# Controls a session with the robot - is the user able to send data to the robot?
#
class Session:
    #Initialise
    def __init__(self):
        #
        # We need to load the xml session file to get the required information
        #
        xmlobj = XMLObject('session.xml')
        #Retreive session data from the xml file
        pass_parent = xmlobj.elementsByTagName('password')[0]
        _pass_value = pass_parent.getElementsByTagName('value')[0].childNodes[0].data
        _pass_req = pass_parent.getElementsByTagName('required')[0].childNodes[0].data
        #Holds connected clients
        self.connections = [];
        #The password to authorise communicating with the robot
        self.password = str(_pass_value)
        #Is the password required for this session?
        self.required = _pass_req
        #Client limit
        self.limit = 10;
    #Checks if the connected ip is authorised
    def isAuth(self,ip):
        print "Connected IP: " + ip

        #Is this the first client to connect to the server?
        if(self.connections==[]):
            print "this is the first connected client"
            return "NO"
        else:
            #Cycle through and check the clients that have tried to connect this session
            for connection in self.connections:
                #Has the client already tried to connect this session?
                if(connection==ip):
                     print "Client has already connected this session"
                     return "YES"
                else:
                     print "This is a new client"
                     return "NO"
        print "Already authenticated..."
        return "YES"
    #Checks if the given password is valid
    def checkPassword(self,jsonobj,connected_ip):
        #
        #We need the password from the JSON object
        #
        _pass = jsonobj.getData('attribute');
        print "checking given password: " + _pass
        
        print "Checking given password"
        if( (_pass == self.password)):
            print "Password is correct"
            self.connections.append(connected_ip);
            return "YES"
        else:
            print "Password is not correct"
            return "NO"
#
# Handles reading/writing of robot programs
#
class Program:
    #init
    def __init__(self):
        print "Created program class"
    #Write application data to file
    def Save(self,appdata):
        #Get the application name
        _name = appdata.getData('attribute');
        #Get the application data
        _data = appdata.getData('value');
        #
        # Print for debugging
        #
        print "--- SAVING PROGRAM ---"
        print "Name: " + _name;
        print "Data: " + _data;
        appdata.Write(_name,"workspace/");
    #Open application data from file
    def Open(self,appname):
        _json = OpenJSON(appname,"workspace/")
    #Return a JSON object containing currently saved applications
    def getSaved(self):
        #array to hold final applications
        data = {}
        #Found applications array
        data['applications'] = []

        #Cycle through the workspace
        for file in os.listdir("workspace/"):
            #Is the file appropriate?
            if file.endswith(".json"):
                #Print for debugging
                print(file)
                #Append to the array
                data['applications'].append(str.split(file,".")[0])
        #Return as JSON data
        return json.dumps(data)
        
        
        
