#!/usr/bin/env python

import web


render = web.template.render('templates/')

urls = (
    '/', 'index'
)




class index:
    def GET(self):
        return render.index('hello world')
        
    
    def POST(self):
        data = web.data()
        print data

if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()

