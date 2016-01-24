#!/usr/bin/env python

from lib.thread import *
from multiprocessing import Process
import threading
from lib.input import *
import time

#
# Import the curses module to accept user input
#
import subprocess

#Class defines a demo
class Demo:
    #Initialise
    def __init__(self,name,func):
        self.name = str(name) #Demo name
        self.func = func #Demo function
        self.isPaused = False
    def Run(self,robot):
        if(self.func!=None):
            if(self.isPaused==False):
                self.isPaused = self.func(robot)
    def Pause(self):
        self.isPaused = True

#
# Define the standard demo functions
#
#Keyboard demo
def func_d_keyboard(robot):
   Keyboard.CheckInput()
   if(Keyboard.IsKeyPressed('w')):
       print "W pressed"
       robot.base._Move(1,0,0)
   elif(Keyboard.IsKeyPressed('a')):
       print "A pressed"
       robot.base._Move(0,1,0)
   elif(Keyboard.IsKeyPressed('s')):
       print "S pressed"
       robot.base._Move(-1,0,0)
   elif(Keyboard.IsKeyPressed('d')):
       print "D pressed"
       robot.base._Move(0,-1,0)
   else:
       robot.Stop()
   #Should this only be run once,if so return true?
   return False
#Hello world demo
def func_d_helloworld(robot):
    os.system('clear')
    print "##############################"
    print "      HELLO WORLD DEMO "
    print "##############################"
    #Show base movements
    #robot.DriveTo(1,0,0)
    #time.sleep(3)
    #robot.Stop()
    #robot.DriveTo(-1,0,0)
    #time.sleep(3)
    #robot.Stop()
    #robot.DriveTo(0,1,0)
    #time.sleep(3)
    #robot.Stop()
    #robot.DriveTo(0,-1,0)
    #time.sleep(3)
    #robot.Stop()
    #Show arm movements
    #unfold arm
    print "Unfolding arm"
    robot.Reach("unfolded")
    robot.Drop()
    print "Folding arm"
    robot.Reach("folded")
    robot.Grab()
    return True
  
d_keyboard = Demo("Keyboard",func_d_keyboard)
d_helloworld = Demo("Helloworld",func_d_helloworld)

#
# Is used to play the given demo -- uses multiprocessing
#
class DemoPlayer:
    #Initialise
    def __init__(self,robot):
        print "Creating demo player"
        self.demo = None
        self.robot = robot
        self.thread = threading.Thread(target=self.Execute,args = (self.robot,))
        self.thread.start()
    def Execute(self,robot):
        while True:
            if(self.demo!=None):
                self.demo.Run(robot)
    #Play the given demo
    def Play(self,demo):
        print "Playing given demo"
        self.demo = demo
    #Stop the current demo
    def Stop(self):
        print "Stopping current demo"
        self.demo = None

#
# Used for storing, and getting demos
#
class DemoStore:
    #Initialise
    def __init__(self):
        print "Creating demo store"
        self.store = [d_keyboard,d_helloworld]
    #Get demo of specified name
    def Get(self,name):
        #Valid given name?
        if(name!=None):
            #State finding demo            
            print "Finding demo using name: " + str(name)
            #Now use the name to get the demo
            for demo in self.store:
                #Check if found demo
                if(str(name)==str(demo.name)):
                    print "Found demo " + str(name) + " !, returning"
                    return demo
            #If we reach this point, the demo was not found - so return None
            print "Couldn't find demo"
            return None
        else:
            print "Cannot find demo with given invalid name"
            return None


#
#Class is used for managing demos
#
class DemoManager:
    #Initialise
    def __init__(self,robot):
        #LOG
        print "Creating demo manager"
        #Demo store holds available demos        
        self.demo_store = DemoStore()
        #Used for playing demos
        self.player = DemoPlayer(robot)
        #The robot using this demo manager
        self.robot = robot
    #Launch demo of given name
    def LaunchDemo(self,name):
        print "Launching demo: " + str(name)
        #Is the given name valid?
        if(name!=None):
            #Try to find, and launch the demo of the given name
            demo = self.demo_store.Get(name)
            if(demo!=None):
                self.player.Play(demo)
    #Stop the current running demo
    def StopDemo(self):
       self.player.Stop()
        
   
    
    
    
    
        