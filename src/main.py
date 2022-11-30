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

config = json.load(open('config.json'))

def hello_function():
    print('Hello Function')

config = json.load(open('config.json'))
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
            return

          

            





    Handler = MyHttpRequestHandler


    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


def open_url():
    webbrowser.open(f'http://localhost:{config.get("server_port",8000)}', new=0, autoraise=True)
    
def runserver(): 
    proc = Popen([f"./main --server"], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    # return proc
    

def runapp(): 
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    runserver()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=open_url).grid(column=1, row=0)


    root.mainloop()

if __name__ == '__main__': 


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
 