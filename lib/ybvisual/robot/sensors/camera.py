#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from cv2 import *
from cv2 import imencode
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import base64



#
# Camera sensor class
#
class Camera:
    #
    # Image class
    #    
    class Img:
        #Initialise
        def __init__(self):
            self.bridge = CvBridge()
            self.image = None
            self.sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)
        #Callback function
        def callback(self,data):
            if data != None:
                self.image = self.bridge.imgmsg_to_cv2(data,"bgr8")
        #If called - return cv2 image
        def __call__(self):
            return self.image #Return the image object
        #Convert the image to a base64 string
        def ToString(self):
            #Check image is not null
            if self.image != None:
                #Convert to byte string
                _str = imencode('.jpg',self.image)[1].tostring()
                #Convert to base64 string
                b64 = base64.encodestring(_str)
                #Return valid
                return str(b64)
            else:
                rospy.loginfo("Invalid image, unable to convert to base64 string")
                #Return invalid
                return ' '
    #Initialise
    def __init__(self,_win):
        rospy.loginfo("Initialised camera sensor")
        #Camera image
        self.image = Camera.Img()
    #Download the image - send back to the clients pc
    def Download(self):
        return self.image.ToString()
