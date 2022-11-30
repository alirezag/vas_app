from tkinter import *
from tkinter import ttk
import webbrowser
from subprocess import Popen
import json

config = json.load(open('config.json'))

def hello_function():
    print('Hello Function')

def open_url():
    webbrowser.open(f'http://localhost:{config.get("server_port",8000)}', new=0, autoraise=True)
    
def run(): 
    proc = Popen([f"python {config.get('server_src','src/server.py')}"], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    return proc
if __name__ == '__main__': 

    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    run()
    ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
    ttk.Button(frm, text="Quit", command=open_url).grid(column=1, row=0)


    root.mainloop()