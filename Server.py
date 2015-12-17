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
        data = web.data()
        print "Received Data: " + data
        controller.Process(data)

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
