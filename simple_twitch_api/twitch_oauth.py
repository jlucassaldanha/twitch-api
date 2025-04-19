import requests
import os, json
import webbrowser

from wsgiref.simple_server import make_server
from wsgiref.util import request_uri


PSEUDO_HTML = [
"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tudo certo!</title>
</head>
<body>
    <a>
        Agora você já pode fechar esta guia...
    </a>
</body>
</html>
""".encode()
            ]
# OU
PSEUDO_HTML = ["Agora você já pode fechar esta guia...".encode()]


OAUTH2_HEADERS = {'Content-Type' : 'application/x-www-form-urlencoded'}

OAUTH2_URL_BASE = "https://id.twitch.tv/oauth2"

oauth_authorize_params = "/authorize?response_type=code&client_id={}&redirect_uri={}&scope={}"

oauth_new_token_data = "client_id={}&client_secret={}&code={}&grant_type=authorization_code&redirect_uri={}"
oauth_refresh_token_data = "grant_type=refresh_token&refresh_token={}&client_id={}&client_secret={}"


class AuthorizationCodeGrantFlow():
    redirect_uri = ""
    url = ""
    client_id = ""
    client_secrets = ""
    query_url = ""
    token_file_data = ""
    access_token = ""
    refresh_token = ""

    def read_credentials_file(self, credentials_json: str) -> None:
        """
        Creates a :class:`AuthorizationCodeGrantFlow`.

        Args:
            credentials_json (str): The path to the credentials.json
            file that have client information.       
        """

        # Read the credentials file data and check keys    
        with open(credentials_json, 'r') as creds_json:
            creds_data = json.load(creds_json)

        creds_json.close()

        # Verify if got the required keys in the data.
        # Case its True save the values in the variables  
        # Case its False, raise execption
        if ("client_id" in list(creds_data) and "client_secrets" in list(creds_data) 
            and "scopes" in list(creds_data) and "redirect_uri" in list(creds_data)):

            self.client_id = creds_data["client_id"]
            self.client_secrets = creds_data["client_secrets"]
            self.scopes = creds_data["scopes"]
            self.redirect_uri = creds_data["redirect_uri"]

            return creds_data

        else:
            raise Exception("Credentials file missing keys")
    
    def read_token_file(self, token_json: str) -> dict:
        """
        Read token file:

        Args:
            token_json (str): Path to the token json file.

        Returns:
            Token data.
        """
        # Read token
        with open(token_json, 'r') as json_file:
            self.token_file_data = json.load(json_file)
        json_file.close()
        
        # Verify if has necessary keys and save in variables
        if ("access_token" in list(self.token_file_data) and
            "refresh_token" in list(self.token_file_data) and
            "token_type" in list(self.token_file_data)):
            self.access_token = self.token_file_data["access_token"]
            self.refresh_token = self.token_file_data["refresh_token"]

            self.valid_token = self.validate_token(self.access_token)

            return self.token_file_data
        else:
            raise Exception("Token file missing keys")
     
    def _localServerApp(self, environ, start_response):
        """
        Creat local server app.
        """
        status = "200 OK"
        headers = [(
            "Content-type", 
            "text/html; charset=utf-8"
            )]  
        
        start_response(status, headers)

        self.query_url = request_uri(environ)

        return PSEUDO_HTML

    def local_server_authorization(self) -> str:
        """
        Runs a local server to got the code from teh authorization request

        Returns:
            Oauth code.
        """
        # get port and host from redirect_uri
        _i = len(self.redirect_uri) - self.redirect_uri[::-1].find(":")
        i_ = self.redirect_uri[_i:].find("/")
        port = int(self.redirect_uri[_i:][:i_])

        __i = self.redirect_uri.find("//") + 2
        i__ = len(self.redirect_uri[__i:]) - len(self.redirect_uri[_i:]) - 1
        host = self.redirect_uri[__i:][:i__]

        server = make_server(host, port, self._localServerApp)

        # Cronstruct the scopes string                
        scopes = self.scopes[0]
        for scope in self.scopes[1:]:
            scopes += "%20" + scope

        # construct the link to the authorization page.
        self.url = OAUTH2_URL_BASE + oauth_authorize_params.format(self.client_id, self.redirect_uri, scopes)

        try:
            # Open the link
            webbrowser.open(self.url)
            
            # Run the server until recive a data
            server.timeout = None
            server.handle_request()

            # Get the part of the url with the parameters
            r = self.query_url

        finally:
            server.server_close()
            
            # try to find code
            i = r.find("?code=")

            # Case got a error response i will be -1
            if i == -1:
                i = r.find("?error=")

                raise Exception("Error in the user Authorization:\n"+r[i:])
            
            else:
                scope_i = r[i:].find("&scope=")
                code_i = 6
                self.oauth_code = r[i:][code_i:scope_i] 
                
                return self.oauth_code

    def create_refresh_token(self, code: str = None, refresh_token: str = None) -> dict:
        """
        Create a new token:
        
        Args:
            code (str) = None: Code give by the authorization screen 
            when run ´openLocalServerAuthorization´.
            refresh_token (str) = None: Code to refresh the token.

        Save data in token.json.

        Returns:
            New token data.
        """
        # Construct links to request
        url = OAUTH2_URL_BASE + "/token"

        # Verify if its a token creation or refresh
        if code != None and refresh_token == None:
            data = oauth_new_token_data.format(self.client_id, self.client_secrets, code, self.redirect_uri)

        if refresh_token != None and code == None:
            data = oauth_refresh_token_data.format(refresh_token, self.client_id, self.client_secrets)

        r = requests.post(url, data, headers=OAUTH2_HEADERS)

        # Verify if request succed, case True, verify keys and so on
        # save data in the token.json file
        if r.status_code == 200:
            token_data = r.json()
            if ("access_token" in list(token_data) and 
                "refresh_token" in list(token_data) and 
                "token_type" in list(token_data)):

                with open("token.json", 'w') as token_json:
                    json.dump(token_data, token_json)
                token_json.close()

                return token_data # return
            
            else:
                raise Exception("Token data missing keys")
            
        else:
            raise Exception("HTTPS response error:\nError getting authorization token")            
        
    def validate_token(self, token: str) -> dict:
        """
        Validate the token:

        Args:
            token (str): Token provided by the oauth.

        Returns:
            If token is valid, return client data, 
            else, return False.
        """
        # URL
        url = OAUTH2_URL_BASE + "/validate"
        # params
        headers = {"Authorization": f"OAuth {token}"}

        r = requests.get(url, headers=headers)

        # Verify if got a response
        if r.status_code == 200:
            token_data = r.json()
            if "client_id" in list(token_data):
                return token_data
            
            else:
                raise Exception("Token file missing keys")
            
        if r.status_code == 401:
            return False
       

# Checklist de funções:
# __init__ - OK
# _localServerApp e local_server_authorization - OK
# create_refresh_token - OK
# validate_token - OK


class TwitchOAuth():
    def __init__(self):  
        pass
