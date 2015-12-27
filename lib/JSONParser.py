#!/usr/bin/env python
import json

#
# JSON Object
#
class JSONObject:
    #Initialise
    def __init__(self,_jsondata):
        self.data = json.loads(_jsondata)
        print "Created JSON object"
    #Get JSON attribute
    def getData(self,att):
        return self.data[att];
    #Write the json object to file
    def Write(self,filename,workspace_folder):
        with open(workspace_folder + filename + ".json","w") as outfile:
            json.dump(self.data,outfile);    

#
# Read JSON from file -- and return a new JSON Object
#
def OpenJSON(filename,workspace_folder):
    _json = JSONObject(open(workspace_folder + filename + ".json").read())
    print "Read JSON from file"
    print _json
    return _json
    
