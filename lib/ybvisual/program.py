#!/usr/bin/env python

from lib.ybvisual.xmlparser import *
import os
import json


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
