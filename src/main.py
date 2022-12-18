from tkinter import *
from tkinter import ttk
import webbrowser
from subprocess import Popen
import json
import argparse
import http.server
import socketserver
from multiprocessing import Process
import json
import platform
from datetime import datetime
import os

config = json.load(open('src/config.json'))

def hello_function():
    print('Hello Function')

PORT=config.get('server_port',8000)

def setup_server():
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
            if not os.path.isdir('results'):
                os.makedirs('results')
            open(os.path.join('results',str(datetime.now()).replace(' ','_') + '.json'),'w').write(output)
            return

          

            





    Handler = MyHttpRequestHandler


    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at url", f"http://localhost:{PORT}")
        httpd.serve_forever()


def open_url():
    webbrowser.open(f'http://localhost:{config.get("server_port",8000)}', new=0, autoraise=True)
    
def runserver(): 
    path = "./dist/main"
    if platform.system() == "Windows": 
        path = ".\dist\windows\main\main"

        Popen([f"cd"], shell=True,
                stdin=None, stdout=None, stderr=None, close_fds=True)
    else: 
        Popen([f"pwd"], shell=True,
                stdin=None, stdout=None, stderr=None, close_fds=True)

    proc = Popen([path, "--server"], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    # return proc
    

def runapp(): 
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    runserver()
    ttk.Label(frm, text="Welcome to VAS Launcher").grid(column=0, row=0)
    ttk.Button(frm, text="Launch", command=open_url).grid(column=1, row=0)


    root.mainloop()

if __name__ == '__main__': 

    print('current dir:', os.getcwd())
    parser = argparse.ArgumentParser(
                    prog = 'VAS APP',
                    description = 'Assessment of Intelligbility of Speech',
                    epilog = 'Thanks for using this program. For any inquery contact Alireza Goudarzi: alireza.goudarzi@gmail.com.')
    
    parser.add_argument('-s', '--server', action='store_true')  # on/off flag
    args = parser.parse_args()

    if args.server: 
        setup_server()
    else:
        runapp()
 