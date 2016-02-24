#!/usr/bin/env python

from lib.ybvisual.xmlparser import *
import os
import json


#
# Handles reading/writing of robot programs
#
class Application:
    #init
    def __init__(self):
        print "Created application class"
        self.workspace = "workspace/"
    #Write application data to file
    def Save(self,appdata,appname):
        if(appdata!=None and appname!=None):
            #
            # Print for debugging
            #
            print "--- SAVING APPLICATION ---"
            print "Name: " + appname;
            print "Data: " + appdata;
            
            #Try and save the application
            with open(self.workspace + str(appname) + ".xml","w") as f:
                f.write(str(appdata))
            print "Applcation saved to file"
        else:
            rospy.logerr("Error saving application")
    #Open application data from file
    def Open(self,appname):
        #_json = OpenJSON(appname,"workspace/")
        _xml = XMLObject.fromFile(self.workspace + appname + ".xml")
        #Attempt to return as a string
        if(_xml!=None):
            return _xml.toString()
        else:
            return " "
    #Return a JSON object containing currently saved applications
    def getSaved(self):
        #array to hold final applications
        data = {}
        #Found applications array
        data['applications'] = []

        #Cycle through the workspace
        for file in os.listdir("workspace/"):
            #Is the file appropriate?
            if file.endswith(".xml"):
                #Print for debugging
                print(file)
                #Append to the array
                data['applications'].append(str.split(file,".")[0])
        #Return as JSON data
        return json.dumps(data)
