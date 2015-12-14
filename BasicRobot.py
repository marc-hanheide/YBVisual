#!/usr/bin/env python
import json


class JSONObject:
    #Initialise
    def __init__(self,_jsondata):
        self.data = json.loads(_jsondata)
        print "Created JSON object"
    def getData(self,att):
        return self.data[att];
    


class RobotController:
    #Initialise
    def __init__(self):
        self.Processing = False;
    #Process incoming data
    def Process(self,data):
        #Create JSON object using given data
        json = JSONObject(data);
        #Get the commands from the json data
        commands = json.getData('commands');
        #Cycle through, and manage the given commands
        for command in commands:
            #
            # We may get, and print command info 
            #
            _command = JSONObject(command);
            _type = _command.getData('type');
            _att = _command.getData('attribute');
            _val = _command.getData('value');
            print "Command Given"
            print "TYPE: "  + _type;
            print "ATTRIBUTE: " + _att;
            print "VALUE: " + _val;
       

            #
            # Now we need to check the given type, and use the data appropriately
            #
            if(_type == "APPDATA"):
                # -- Now process the application data, and save it to file
                xml_file = open(_data + ".xml","wb");
                xml_file.write(_data02);
                xml_file.close();
                print xml_file
            #Move type command
            if(_type == "MOVE"):
                    print "Move command";
                    if(_att == "FORWARD"):
                        print "Move forward command";
                        #Process the data here - move the robot forward
                    if(_att == "BACK"):
                        print "Move backward command";
                        #Move the robot back
                    if(_att == "LEFT"):
                        print "Move left command";
                        #Move the robot left
                    if(_att == "RIGHT"):
                        print "Move right command";
                        #Move the robot right
            #Rotate type command
            if(_type == "ROTATE"):
                    if(_att == "RIGHT"):
                        print "Rotate right command";
                        #Rotate the robot right
                    if(_att == "LEFT"):
                        print "Rotate left command";
                        #Rotate the robot left
                
            
        
