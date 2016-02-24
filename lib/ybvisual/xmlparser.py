#!/usr/bin/env python

from xml.dom.minidom import parse,parseString
import xml.etree.ElementTree as et
import xml.dom.minidom

#
# XML Object
#
class XMLObject:
    def __init__(self,data):
        self.data = data
    def toString(self):
        if(self.data!=None):
            _str = self.data.toprettyxml()
            print("Conveted xml to string: " + str(_str))
            return _str
        else:
            return None
    @staticmethod
    #Load XML data from a string
    def fromString(string):
        if(string!=None):
            data = parseString(str(string))
            print "Created XML object from string: " + str(string)
            return XMLObject(data)
        else:
            return None
    @staticmethod
    #Load XML data from file
    def fromFile(src):
        if(src!=None):
            data = parse(src)
            print "Created XML object from file: " + src
            return XMLObject(data)
        else:
            return None
