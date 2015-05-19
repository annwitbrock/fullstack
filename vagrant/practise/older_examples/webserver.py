from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

from restaurant import *

class webServerHandler(BaseHTTPRequestHandler):
    def success_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('X-Clacks-Overhead', 'GNU Terry Pratchett')
        self.end_headers()
        
    def restaurant_header(self):
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurants')
        self.send_header('X-Clacks-Overhead', 'GNU Terry Pratchett')
        self.end_headers()
                
    def html_output(self, template):
        output = ""
        html = "<html><head></head> <body>%s"
        html += "</body></html>"
        output += html % (template,)

        self.wfile.write(output)
        #print output
    
    def hello_template(self, content):
        html = "%s"
        html += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
        html += "<h2>What shall I say?</h2>"
        html += "<input name='message' type='text' />"
        html += "<input type='submit' value='Submit' />"
        html += "</form>"
        output =  html % (content,)

        return output
        
    def new_restaurant_template(self):
        html = "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
        html += "<h2>What is the name of the new restaurant?</h2>"
        html += "<input name='restaurant_name' type='text' />"
        html += "<input type='submit' value='Submit' />"
        html += "</form>"

        return html
        
    def edit_restaurant_template(self, restaurantid, oldname):
        html = "<form method='POST' enctype='multipart/form-data' action='/restaurants/"
        html += restaurantid
        html += "/edit'>"
        html += "<h2>What is the new name for %s?</h2>" % oldname
        html += "<input name='restaurant_new_name' type='text' />"
        html += "<input type='submit' value='Change' />"
        html += "</form>"
        
        print html
        return html
        
    def delete_restaurant_template(self, restaurantid, name):
        html = "<form method='POST' enctype='multipart/form-data' action='/restaurants/"
        html += restaurantid
        html += "/delete'>"
        html += "<h2>Are you sure you want to delete %s?</h2>" % name
        html += "<input type='submit' value='Delete' />"
        html += "<a href='/restaurants'>Cancel</a>"
        html += "</form>"

        print html
        return html
        
    def restaurant_template(self, content):
        html = "<div><a href='/restaurants/new'>Add a new restaurant</a></div>"
        for restaurant in content:
            item = "%s"
            item += "</br>"
            item += "<a href='/restaurants/%s/edit'>Edit</a>"
            item += "</br>"
            item += "<a href='/restaurants/%s/delete'>Delete</a>"
            item += "</br>"
            html += item % (restaurant.name, restaurant.id, restaurant.id)

        #print html
        return html
        
    def id_from_path(self, s):
        return s[s.index('/',1) + 1 : s.rindex('/')]

    
    def do_GET(self):
        try:
            print "Get", self.path
            if self.path.endswith('/restaurants'):
                self.success_header()
                names = restaurants()
                self.html_output(self.restaurant_template(names))
                return
            if self.path.endswith('/restaurants/new'):
                self.success_header()
                self.html_output(self.new_restaurant_template())
                return
            if self.path.endswith('/edit'):
                rest_id = self.id_from_path(self.path)
                restaurant = restaurantById(rest_id)

                self.success_header()
                self.html_output(self.edit_restaurant_template(rest_id, restaurant.name))
                return
            if self.path.endswith('/delete'):
                rest_id = self.id_from_path(self.path)
                restaurant = restaurantById(rest_id)
                
                self.success_header()
                self.html_output(self.delete_restaurant_template(rest_id, restaurant.name))
                return
            if self.path.endswith('/hello'):
                self.success_header()
                self.html_output(self.hello_template("hello!"))
                return
            if self.path.endswith('/hola'):
                self.success_header()
                self.html_output(self.hello_template("&#161Hola <a href='/hello' >Back to Hello</a>"))
                return
        except:
            self.send_error(404, "File not found %s" % self.path)
        
    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')
                    addNewRestaurant(messagecontent[0])
                    
                    self.restaurant_header()
                    return
            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_new_name')
                    rest_id = self.id_from_path(self.path)
                    editRestaurantById(rest_id, messagecontent[0])
                    
                    self.restaurant_header()
                    return
            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    rest_id = self.id_from_path(self.path)
                    deleteRestaurantById(rest_id)
                    
                    self.restaurant_header()
                    return
            else:
                self.send_response(301)
                self.end_headers()
                
                messagecontent = ""
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                
                    content = "<h2>OK how about this?</h2><h1> %s </h1>" % (messagecontent[0],)
                    self.html_output(self.hello_template(content))
        except:
            self.send_error(404, "Post unsuccessful %s" % self.path)

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web server running on Port %s" % port
        server.serve_forever()
        
    except KeyboardInterrupt:
        print "Ctl C, now stopping web server"
        server.socket.close()

if __name__ == '__main__':
    main()
