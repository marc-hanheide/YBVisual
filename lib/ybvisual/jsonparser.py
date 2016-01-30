#!/usr/bin/env python
import json

#
# JSON Object
#
class JSONObject:
    #Initialise
    def __init__(self,_jsondata):
        self.data = json.loads(_jsondata)
        #print "Created JSON object"
    #Get JSON attribute
    def getData(self,att):
        return self.data[att];
    #Write the json object to file
    def Write(self,filename,workspace_folder):
        with open(workspace_folder + filename + ".json","w") as outfile:
            json.dump(self.data,outfile);
    @staticmethod
    #Check if received data is of given type
    def IsType(data_json,__type):
        #Only attempt if the given data is not null
        if(data_json!=None):
            #Get the type
            _type = data_json.getData('type')
            #Check the type
            if(_type == str(__type)):
                return True
            else:
                return False
    @staticmethod
    #Check if the received data has given attribute
    def HasAttribute(data_json,__att):
        #Only attempt if the given data is not null
        if(data_json!=None):
            #Get the attribute
            _att = data_json.getData('attribute')
            #Check the attribute
            if(_att == str(__att)):
                return True
            else:
                return False
    @staticmethod
    #Check if the received data has given value
    def HasValue(data_json,__val):
        #Only attempt if the given data is not null
        if(data_json!=None):
            #Get the value
            _val = data_json.getData('value')
            #Check the value
            if(_val== str(__val)):
                return True
            else:
                return False

#
# Read JSON from file -- and return a new JSON Object
#
def OpenJSON(filename,workspace_folder):
    _json = JSONObject(open(workspace_folder + filename + ".json").read())
    print "Read JSON from file"
    print _json
    return _json
    
