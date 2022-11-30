import http.server
import socketserver
from multiprocessing import Process
import json
import os
# class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.path = 'index.html'
#         return http.server.SimpleHTTPRequestHandler.do_GET(self)
config = json.load(open('config.json'))
PORT=config.get('server_port',8000)

def f():
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):

        def do_GET(self):
            # self.path = os.path.join(config.get('app_dir','./app'),self.path)
            # self.path = "./app/"+self.path
            self.path = config.get('app_dir','./app') + self.path
            super().do_GET()
           

        def do_POST(self): 
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            print(json.loads(post_body.decode()))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            output = json.dumps({"result" : post_body.decode()})
            self.wfile.write(output.encode())
            print(output)
            return

          

            





    Handler = MyHttpRequestHandler


    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

if __name__=='__main__': 
   f()

