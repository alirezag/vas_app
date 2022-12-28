from enum import Enum
from http import HTTPStatus
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import webbrowser
from subprocess import Popen
import json
import argparse
import http.server
import socketserver
import platform
import os
import email.utils
import urllib.parse
import datetime

# the keys stimuli directory dictionary.
class StimuliPathKey(str,Enum):
    """
    The keys stimuli directory dictionary.
    """
    # the key for the stimuli directory.
    STIMULI = 'stimuli'
    RELIABILITY = 'reliability'
    MSG = 'message'
    LAUNCH = 'launch'


# path to the stimuli directory, set by user
STIMULI_DIR = { }
STIMULI_DIR_LABELS = {}

# set up the prefix path.
DIRPREFIX = ''
if os.path.isdir('src'):
    DIRPREFIX = 'src/'

# load the config file
config = json.load(open(f'{DIRPREFIX}config.json'))


def hello_function():
    """_summary_
    only for testing
    """
    print('Hello Function')

# parser the server port
PORT=config.get('server_port',8000)

def setup_server():
    """
    Setup server
    """
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        """Implementation of HTTP request handler class with GET and HEAD commands."""
        
        
        def send_head(self, no_translate=True):
            """Common code for GET and HEAD commands.

            This sends the response code and MIME headers.

            Return value is either a file object (which has to be copied
            to the outputfile by the caller unless the command was HEAD,
            and must be closed by the caller under all circumstances), or
            None, in which case the caller has nothing further to do.

            """
            if no_translate: 
                path = self.path
            else:
                path = self.translate_path(self.path)

               
            f = None
            if os.path.isdir(path):
                parts = urllib.parse.urlsplit(self.path)
                if not parts.path.endswith('/'):
                    # redirect browser - doing basically what apache does
                    self.send_response(HTTPStatus.MOVED_PERMANENTLY)
                    new_parts = (parts[0], parts[1], parts[2] + '/',
                                parts[3], parts[4])
                    new_url = urllib.parse.urlunsplit(new_parts)
                    self.send_header("Location", new_url)
                    self.send_header("Content-Length", "0")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    return None
                for index in "index.html", "index.htm":
                    index = os.path.join(path, index)
                    if os.path.exists(index):
                        path = index
                        break
                else:
                    return self.list_directory(path)
            ctype = self.guess_type(path)
            # check for trailing "/" which should return 404. See Issue17324
            # The test for this was added in test_httpserver.py
            # However, some OS platforms accept a trailingSlash as a filename
            # See discussion on python-dev and Issue34711 regarding
            # parseing and rejection of filenames with a trailing slash
            if path.endswith("/"):
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return None
            try:
                # print(path)
                f = open(path, 'rb')
            except OSError:
                self.send_error(HTTPStatus.NOT_FOUND, "File not found")
                return None

            try:
                fs = os.fstat(f.fileno())
                # Use browser cache if possible
                if ("If-Modified-Since" in self.headers
                        and "If-None-Match" not in self.headers):
                    # compare If-Modified-Since and time of last file modification
                    try:
                        ims = email.utils.parsedate_to_datetime(
                            self.headers["If-Modified-Since"])
                    except (TypeError, IndexError, OverflowError, ValueError):
                        # ignore ill-formed values
                        pass
                    else:
                        if ims.tzinfo is None:
                            # obsolete format with no timezone, cf.
                            # https://tools.ietf.org/html/rfc7231#section-7.1.1.1
                            ims = ims.replace(tzinfo=datetime.timezone.utc)
                        if ims.tzinfo is datetime.timezone.utc:
                            # compare to UTC datetime of last modification
                            last_modif = datetime.datetime.fromtimestamp(
                                fs.st_mtime, datetime.timezone.utc)
                            # remove microseconds, like in If-Modified-Since
                            last_modif = last_modif.replace(microsecond=0)

                            if last_modif <= ims:
                                self.send_response(HTTPStatus.NOT_MODIFIED)
                                self.end_headers()
                                f.close()
                                return None

                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", ctype)
                self.send_header("Content-Length", str(fs[6]))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Last-Modified",
                    self.date_time_string(fs.st_mtime))
                self.end_headers()
                return f
            except:
                f.close()
                raise
            
        def do_GET(self):
            # self.path = os.path.join(config.get('app_dir','./app'),self.path)
            # self.path = "./app/"+self.path
            f=None
            if self.path.startswith('/audio'):
                self.path = urllib.parse.unquote(self.path)
                STIMULI_DIR.update(json.load(open('data.json','r')))
                if self.path.startswith('/audio/stimuli'):
                    self.path = self.path.replace('/audio/stimuli','')
                    self.path = STIMULI_DIR[StimuliPathKey.STIMULI] + self.path
                elif self.path.startswith('/audio/reliability'):
                    self.path = self.path.replace('/audio/reliability','')
                    self.path = STIMULI_DIR[StimuliPathKey.RELIABILITY] + self.path 
                f = self.send_head(no_translate=True)
            else:
                self.path = config.get('app_dir','./app') + self.path
                f = self.send_head()
            # print(self.path)
            
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()


        def do_POST(self):
            content_len = int(self.headers.get('Content-Length'))
            post_body = self.rfile.read(content_len)
            # print(json.loads(post_body.decode()))

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            output = json.dumps({"result" : post_body.decode()})
            self.wfile.write(output.encode())
            # print(output)
            if not os.path.isdir('results'):
                os.makedirs('results')
            open(os.path.join('results',str(datetime.datetime.now()).replace(' ', '_').replace(':','-') + '.json'), 'w').write(output)
            return


    Handler = MyHttpRequestHandler


    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at url", f"http://localhost:{PORT}")
        httpd.serve_forever()


def open_url():
    webbrowser.open(f'http://localhost:{PORT}', new=0, autoraise=True)

def get_path(key:StimuliPathKey): 
    assert key in [StimuliPathKey.RELIABILITY, StimuliPathKey.STIMULI]
    try: 
        STIMULI_DIR[key] = filedialog.askdirectory()
        STIMULI_DIR_LABELS[key].config(text=STIMULI_DIR[key])
    except Exception as E:
        print("error",E )

    if STIMULI_DIR[StimuliPathKey.STIMULI] and STIMULI_DIR[StimuliPathKey.RELIABILITY]:
        STIMULI_DIR_LABELS[StimuliPathKey.LAUNCH].config(state=NORMAL)
        STIMULI_DIR_LABELS[StimuliPathKey.MSG].config(text="Now you can launch the app.")
        with open('data.json','w') as f:
            json.dump(STIMULI_DIR,f)

    

def runserver():
    path = "./dist/main"
    if platform.system() == "Windows":
        path = ".\dist\windows\main\main"

        Popen([f"cd"], shell=True,
                stdin=None, stdout=None, stderr=None, close_fds=True)
    else:
        Popen([f"pwd"], shell=True,
                stdin=None, stdout=None, stderr=None, close_fds=True)

    Popen([path, "--server"], shell=True,
             stdin=None, stdout=None, stderr=None, close_fds=True)


def runapp():
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    runserver()
    ttk.Label(frm, text="Welcome to VAS Launcher").grid(column=0, row=0)
    STIMULI_DIR_LABELS[StimuliPathKey.LAUNCH] = ttk.Button(frm, text="Launch", command=open_url, state='disabled')
    STIMULI_DIR_LABELS[StimuliPathKey.LAUNCH].grid(column=1, row=0)
    STIMULI_DIR_LABELS[StimuliPathKey.MSG] = ttk.Label(frm, text="Select paths to continue.")
    STIMULI_DIR_LABELS[StimuliPathKey.MSG].grid(column=0, row=1)
    
    STIMULI_DIR_LABELS[StimuliPathKey.STIMULI] = ttk.Label(frm, text="Select the path to stimuli")
    STIMULI_DIR_LABELS[StimuliPathKey.STIMULI].grid(column=0, row=2)
    ttk.Button(frm, text="Select", command= lambda : get_path(StimuliPathKey.STIMULI)).grid(column=1, row=2)
    STIMULI_DIR_LABELS[StimuliPathKey.RELIABILITY] = ttk.Label(frm, text="Select the path to reliability stimuli")
    STIMULI_DIR_LABELS[StimuliPathKey.RELIABILITY].grid(column=0, row=3)
    ttk.Button(frm, text="Select", command= lambda : get_path(StimuliPathKey.RELIABILITY)).grid(column=1, row=3)


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
 