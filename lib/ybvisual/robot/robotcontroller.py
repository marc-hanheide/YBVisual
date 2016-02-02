#!/usr/bin/env python
import rospy
from lib.ybvisual.jsonparser import JSONObject
import time
from lib.ybvisual.demomanager import DemoManager
from threading import Thread

#
# We need to import the main robot script
#
from lib.ybvisual.robot.robot import Robot
    
#
# Robot controller
#
class RobotController:
    #Initialise
    def __init__(self):
        #Define the youbot object
        self.robot = Robot();
        #Demo manager
        self.demo_manager = DemoManager(self.robot)
        self.data = None
        self.EMERGENCY_STOP = False
        #Thread used for processing data
        self.thread = Thread(target=self._ThreadFunc,args = ())
        #Start process data checks
        self.Start()
    #Halt execution -- acts as an emergency stop
    def Halt(self):
        self.robot.EmergencyStop()
    #Process incoming data
    def Process(self,data):
        #Create JSON object using given data
        #json_data = JSONObject(data);
        
        #Get the commands from the json data
        #commands = json.getData('commands');
        commands_json = JSONObject(data.getData('attribute'))
        commands = commands_json.getData('commands')

        #These variables are used to check for a condition
        condition_current = ' ' #The current condition to check
        condition_valid = True #The result of the condition
    
        
        #Cycle through, and manage the given commands
        for command in commands:
            #Ensure the robot is stopped before running more commands
            self.robot.Stop()               
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

            #Print the status of the gripper - for debugging
            self.robot.PrintGripperStatus()

            
            
            #Check if the given data is a condition
            if(_type == "COND"):
                rospy.loginfo("Found condition")
                #Initially - the condition isn't valid
                condition_valid = False
                #Check the type of the condition
                if(_att == "GRIPPERSTATE"):
                    rospy.loginfo("Gripper state condition")
                    #Check the state of the gripper
                    #Which state are we checking for?
                    state_check = str(_val)
                    if(state_check=="OPEN"):
                        print "Checking gripper open condition"
                        #Check if the gripper is open
                        if(self.robot.IsGripperOpen()):
                            #Gripper is open
                            condition_valid = True
                    elif(state_check=="CLOSED"):
                        print "Checking gripper closed condition"
                        #Check if the gripper is closed
                        if(self.robot.IsGripperClosed()):
                            #Gripper is closed
                            condition_valid = True
                            
            #We may carry on if condition is valid
            if(condition_valid == True):
                rospy.loginfo("Condition is valid, executing command..")
            
            #
            # Now we need to check the given type, and use the data appropriately
            #
            #Application request command
                if(_type == "APPDATA"):
                    # -- Now process the application data, and save it to file
                    xml_file = open(_data + ".xml","wb");
                    xml_file.write(_data02);
                    xml_file.close();
                    print xml_file
                #Demo request command
                if(_type == "DEMO"):
                    print "Demo command"
                    # -- Demo start
                    if(_att == "START"):
                        print "Demo start request"
                        #Get the demo name
                        name = str(_val)
                        rospy.loginfo("Trying to start demo using given name: " + str(_val))
                        self.demo_manager.LaunchDemo(name)
                    # --Demo stop
                    if(_att == "STOP"):
                        print "Demo stop request"
                        #Stop the currently running demo
                        self.demo_manager.StopDemo()
                        Keyboard.Restore()
            
                #Move type command
                if(_type == "MOVE"):
                        print "Move command";
                        #Get amount value
                        amount = float(int(_val));
                        print "Amount: " + str(amount);
                        self.robot.DriveByCmd(str(_att),amount)
                #Rotate type command
                if(_type == "ROTATE"):
                        #Get amount value
                        amount = float(int(_val));
                        print "Amount: " + str(amount);
                        self.robot.RotateByCmd(str(_att),amount)
                #Move arm type command
                if(_type == "MOVEARM"):
                        #Is this is a 'move to pre-defined position' command?
                        if(_att == "DEFPOS"):
                            #If so - attempt to move the robot to the given position name
                            #self.robot.arm.ToStandardJointSpaceGoal(str(_val))
                            self.robot.arm.MoveTo(str(_val))
                #Rotate joint command
                if(_type == "ROTATEJOINT"):
                        #Rotate the joint
                        joint_name = str(_att)
                        value = float(_val)
                        self.robot.arm.SetJointValue(self.robot.arm.JointIdByName(joint_name),value)
                #Set gripper command
                if(_type =="GRIPPER"):
                        #What type of gripper command is this?
                        #Set gripper status command
                        if(_att == "SET"):
                            #Has the user chosen to open, or close the gripper?
                            choice = str(_val)
                            if(choice == "OPEN"):
                                self.robot.Drop()
                            elif(choice == "CLOSE"):
                                 self.robot.Grab()
            
                #halt type command
                if(_type == "HALT"):
                    print "Halt command";
                    self.robot.Stop();
                
                #Process a util command
                if(_type == "UTIL"):
                    print "Util command"
                    #Wait command
                    if(_att == "WAIT"):
                        #Get the wait time
                        _time = int(_val)
                        print "Waiting for.." + str(_time) + " seconds"
                        time.sleep(_time)
                        print "Finished waiting!"
                #Pause before starting next command
                rospy.sleep(0.2);
            else:
                print "Unable to execute command.. condition is not valid"
                
        #Stop the robot once execution has finished
        self.robot.Stop();
        #Reset data
        self.data = None
    #Set data
    def SetData(self,data):
        rospy.loginfo("Setting process data")
        if(data!=None):
            self.data = data
    #Thread function
    def _ThreadFunc(self):
        while True:
            if self.data != None:
                rospy.loginfo("Found process data")
                self.Process(self.data)
                time.sleep(1)
    #Start processing data
    def Start(self):
        rospy.loginfo("Starting process thread")
        self.thread.deamon = True
        self.thread.start()
    def Shutdown(self):
        rospy.signal_shutdown("Done!")
