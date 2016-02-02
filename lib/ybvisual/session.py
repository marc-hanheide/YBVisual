#!/usr/bin/env python

from lib.ybvisual.xmlparser import *
import os
import json

#
# Global variables for use with the server console
#
ACCEPTED_CONNECTIONS = []


#
# Controls a session with the robot - is the user able to send data to the robot?
#
class Session:
    #Initialise
    def __init__(self):
        #
        # We need to load the xml session file to get the required information
        #
        xmlobj = XMLObject('lib/session.xml')
        #Retreive session data from the xml file
        pass_parent = xmlobj.elementsByTagName('password')[0]
        _pass_value = pass_parent.getElementsByTagName('value')[0].childNodes[0].data
        _pass_req = pass_parent.getElementsByTagName('required')[0].childNodes[0].data
        #Also need to retreive the admin password        
        admin_pass_parent = xmlobj.elementsByTagName('admin_password')[0]
        _admin_pass_value = admin_pass_parent.getElementsByTagName('value')[0].childNodes[0].data
        print "ADMIN PASSWORD: " + _admin_pass_value        
        
        #Holds connected clients
        self.connections = [];
        #The password to authorise communicating with the robot
        self.password = str(_pass_value)
        #This is the required password for accessing the console        
        self.admin_password = str(_admin_pass_value)
        #Is the password required for this session?
        self.required = _pass_req
        #Client limit
        self.limit = 10;
    #Checks if the connected ip is authorised
    def isAuth(self,ip):
        #print "Connected IP: " + ip

        #Is this the first client to connect to the server?
        if(self.connections == []):
            #print "this is the first connected client"
            #self.listConnections()
            return "NO"
        else:
            #Cycle through and check the clients that have tried to connect this session
            for connection in self.connections:
                #Has the client already tried to connect this session?
                if(connection==str(ip)):
                     #print "Client has already connected this session"
                     #self.listConnections()
                     return "YES"
                else:
                     #print "This is a new client"
                     #self.listConnections()
                     return "NO"
        #print "Already authenticated..."
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
            print "IP added to connections list:" + connected_ip
            self.connections.append(str(connected_ip))
            self.listConnections()
            return "YES"
        else:
            print "Password is not correct"
            return "NO"
    #Checks if the admin password is correct
    def checkAdminPassword(self,jsonobj):
        #
        # Get the admin password from the JSON object
        #
        _pass = jsonobj.getData('attribute');
        print "Checking given admin password: " + _pass
        
        print "Checking against admin password: " + self.admin_password
        #Correct admin password
        if( ( _pass == self.admin_password )):
            print "Password is correct"
            return "YES" #Return valid
        #Incorrect admin password
        else:
            print "Password is not correct"
            return "NO" #Return invalid
    #
    # Print a list of current connections
    #
    def listConnections(self):
        print "Current connections: "
        for connection in self.connections:
            print str(connection)
    #
    # Clear all accepted connections
    #
    def clearConnections(self):
        #Reset the array - it should now be empty
        self.connections = [];
    
    # Get connections as a JSON file
    def getConnections(self):
        #array to hold final applications
        data = {}
        #Found applications array
        data['connections'] = []
        
        for connection in self.connections:
            data['connections'].append(str(connection))
        
        #Return as JSON data
        return json.dumps(data)
    #Remove an active connection from the session
    def removeConnection(self,ip):
        print "Attempting to remove connection: " + str(ip)
        for connection in self.connections:
            if (str(connection)==ip):
                self.connections.remove(connection)

        
        