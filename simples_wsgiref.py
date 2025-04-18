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
    <title>Tudo certo!</title>
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
"""
m = ["The authentication flow has completed. You may close this window.".encode()]
def hello_world_app(environ, start_response):    
    global respostas
    status = "200 OK"  # HTTP Status
    headers = [("Content-type", "text/html; charset=utf-8")]  # HTTP Headers
    start_response(status, headers)
    respostas = request_uri(environ)
    print(respostas)
    # The returned object is going to be printed
    
    return m#teste#[b"Hello World"]

with make_server("", 500, hello_world_app) as httpd:
    print("Serving on port 8000...")

    # Serve until process is killed
    #httpd.serve_forever()
    httpd.handle_request()
    print(httpd.address_family)
    print(httpd.application)
    print(httpd.request_queue_size)
    print(httpd.server_address)
    print(httpd.socket)

httpd.server_close()"""

class serverson():
    def localServerApp(self, environ, start_response):
        status = "200 OK"
        headers = [(
            "Content-type", 
            "text/html; charset=utf-8"
            )]  
        
        start_response(status, headers)

        self.query_url = request_uri(environ)

        return teste

    def openAuthorization(self):

       
        # Cria o app

        # Seta a flag de reuso do endereço com false

        # Cria o server
        server = make_server("", 500, self.localServerApp)

        # Inicia um try

        server.timeout = None
        server.handle_request()

        #timeout server
        #roda uma vez e pega a request

        #pega a resposta
        r = self.query_url

        print(r)


a = serverson()
a.openAuthorization()