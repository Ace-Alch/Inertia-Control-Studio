"""Serve the app locally. Python 3 standard library only."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path
import webbrowser
import threading
root=Path(__file__).resolve().parent
url='http://127.0.0.1:8000/index.html'
server=ThreadingHTTPServer(('127.0.0.1',8000),partial(SimpleHTTPRequestHandler,directory=str(root)))
print('Inertia Control Studio:',url)
print('Press Ctrl+C to stop.')
threading.Timer(.5,lambda:webbrowser.open(url)).start()
try: server.serve_forever()
except KeyboardInterrupt: pass
finally: server.server_close()
