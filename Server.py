#!/usr/bin/env python

import web
from Robot import *


render = web.template.render('templates/')

urls = (
    '/', 'index'
)

controller = RobotController()


class index:
    def GET(self):
        return render.index('hello world')
        
    
    def POST(self):
        if(controller.isProcessing() == False):
            data = web.data()
            print data
            controller.Process(data)
        else:
            print "Still processing";

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
