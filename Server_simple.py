#!/usr/bin/env python

import web


render = web.template.render('templates/')

urls = (
    '/', 'index'
)

current_connections = []



def Auth():
    print "Loaded authentication page"
    #Get the IP of the client trying to connect to the server
    CONNECTED_IP = web.ctx.ip
    print "Connected IP: " + CONNECTED_IP

    #Is this the first client to connect to the server?
    if(current_connections==[]):
        print "this is the first connected client"
        return "NO"
    else:
        #Cycle through and check the clients that have tried to connect this session
        for connection in current_connections:
            #Has the client already tried to connect this session?
            if(connection==CONNECTED_IP):
                 print "Client has already connected this session"
                 return "YES"
            else:
                 print "This is a new client"
                 return "NO"
    print "Already authenticated..."
    return "YES"

def CheckPass(data):
    print "Checking given password"
    if( (data=="KUKA")):
        print "Password is correct"
        current_connections.append(web.ctx.ip);
        return "YES"
    else:
        print "Password is not correct"
        return "NO"
    

class index:
    def GET(self):
        return render.index()
        
    
    def POST(self):
        data = web.data()
        print "Received Data: " + data
        if(data=="AUTHCHECK"):
            return Auth();
        else:
            return CheckPass(data);
            

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
