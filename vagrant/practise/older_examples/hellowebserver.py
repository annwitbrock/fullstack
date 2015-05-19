from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

class webServerHandler(BaseHTTPRequestHandler):
    def success_header(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('X-Clacks-Overhead', 'GNU Terry Pratchett')
        self.end_headers()
                
    def html_output(self, template):
        output = ""
        html = "<html><head></head> <body>%s"
        html += "</body></html>"
        output += html % (template,)

        self.wfile.write(output)
        print output
    
    def hello_template(self, content):
        html = "%s"
        html += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
        html += "<h2>What shall I say?</h2>"
        html += "<input name='message' type='text' />"
        html += "<input type='submit' value='Submit' />"
        html += "</form>"
        output =  html % (content,)
        print output
        return output
    
    def do_GET(self):
        try:
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
            self.send_response(301)
            self.end_headers()
            
            messagecontent = ""
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                
            content = "<h2>OK how about this?</h2><h1> %s </h1>" % (messagecontent[0],)
            print content
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
