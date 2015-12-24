#!/usr/bin/env python

from xml.dom.minidom import parse
import xml.dom.minidom

#
# XML Object
#
class XMLObject:
    #Initailise
    def __init__(self,src):
        DOMTree = xml.dom.minidom.parse(src)
        self.collection = DOMTree.documentElement
        print "Created XML object from file: " + src
    #
    # Get elements inside xml document by their tag names
    #
    def elementsByTagName(self,tag):
        return self.collection.getElementsByTagName(tag)
    
