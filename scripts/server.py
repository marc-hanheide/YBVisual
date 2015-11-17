#!/usr/bin/python

import web
import urllib2

urls = ('/','index')

class index:
    def GET(self):
        print web.data()
        return "Hello world!"
    def POST(self):
        print web.data()

class Server:
    def __init__(self):
        self.ip = '10.169.145.143'
        self.port = 8888
    def Start(self):
        self.app = web.application(urls,globals())
        print "Starting server.."
        web.httpserver.runsimple(self.app.wsgifunc(), (self.ip,self.port))

        
        
if __name__ == '__main__':
    server = Server()
    server.Start()
