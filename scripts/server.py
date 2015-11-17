#!/usr/bin/python

import web

urls = ('/','index')

class index:
    def GET(self):
        print web.data()
        return "Hello world!"
    def POST(self):
        print web.data()
        
        
if __name__ == '__main__':
    app = web.application(urls,globals());
    print "Starting server.."
    web.httpserver.runsimple(app.wsgifunc(), ("10.169.145.143", 8888));
