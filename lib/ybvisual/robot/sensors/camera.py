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
    #Initialise
    def __init__(self,_win):
        #Open a local window to show camera output?
        self._win = _win
        if self._win == True:
            namedWindow("Image",1)
            startWindowThread()
        
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)
        self.cv_image = None
        rospy.loginfo("Initialised camera sensor")
    #Callback function for handling callback data
    def callback(self,data):
        if data != None:
            self.cv_image = self.bridge.imgmsg_to_cv2(data,"bgr8")
            if self._win == True:
                imshow("Image",self.cv_image)
    #Download the image - send back to the clients pc
    def Download(self):
        img_str = ''
        if(self.cv_image!=None):
            img_str = imencode('.jpg',self.cv_image)[1].tostring()
            b64 = base64.encodestring(img_str)
        return str(b64)

#Camera(True)

#rospy.init_node('image')
#rospy.spin()

#destoryAllWindows()
        

