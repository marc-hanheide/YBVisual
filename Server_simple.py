#!/usr/bin/env python

import web
from JSONParser import *
from Session import *

render = web.template.render('templates/')

urls = (
    '/', 'index'
)

#Holds session information
session = Session()


    

class index:
    def GET(self):
        return render.index()
        
    
    def POST(self):
        data = web.data()
        print "Received Data: " + data
        #Create JSON object using given data - if required
        json = JSONObject(data);
        _type = json.getData('type')
        print "Received JSON data with type: " + _type
        #
        # Check if received data is an auth check
        #
        if(_type == 'AUTHCHECK'):
            return session.isAuth(web.ctx.ip)
        #
        # Check if this is a password check
        #
        if(_type == 'PASSCHECK'):
            return session.checkPassword(json,web.ctx.ip)
      

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
