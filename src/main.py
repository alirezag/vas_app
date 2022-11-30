from tkinter import *
from tkinter import ttk
import webbrowser
from subprocess import Popen
import json
import argparse
from .server import setup_server

config = json.load(open('config.json'))

def hello_function():
    print('Hello Function')

def open_url():
    webbrowser.open(f'http://localhost:{config.get("server_port",8000)}', new=0, autoraise=True)
    
def runserver(): 
    proc = Popen([f"main --server"], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    # return proc
    

def runapp(): 
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    run()
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
 