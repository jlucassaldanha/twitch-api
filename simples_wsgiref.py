"""from wsgiref.simple_server import make_server, demo_app

with make_server('', 8000, demo_app) as httpd:
    print("Serving HTTP on port 8000...")

    # Respond to requests until process is killed
    httpd.serve_forever()

    # Alternative: serve one request, then exit
    httpd.handle_request()"""

"""
Every WSGI application must have an application object - a callable
object that accepts two arguments. For that purpose, we're going to
use a function (note that you're not limited to a function, you can
use a class for example). The first argument passed to the function
is a dictionary containing CGI-style environment variables and the
second variable is the callable object.
"""
teste = ["""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <a>
        hello world!
    </a>
</body>
</html>
""".encode()]

##### MUITO INTERESSANTE
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri


def hello_world_app(environ, start_response):    
    global respostas
    status = "200 OK"  # HTTP Status
    headers = [("Content-type", "text/html; charset=utf-8")]  # HTTP Headers
    start_response(status, headers)
    respostas = request_uri(environ)
    print(respostas)
    # The returned object is going to be printed
    
    return teste#[b"Hello World"]

with make_server("", 8000, hello_world_app) as httpd:
    print("Serving on port 8000...")

    # Serve until process is killed
    #httpd.serve_forever()
    httpd.handle_request()