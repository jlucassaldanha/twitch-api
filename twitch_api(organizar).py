import requests
import json
import os
import webbrowser

from wsgiref.simple_server import make_server
from wsgiref.util import request_uri

# usar biblioteca do google de exemplo
# Token e refresh token podem ser mescladas


class TwitchOAuth():
    def __init__(self):  
        pass

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
    redirec_uri = None
    url = None
    client_id = None
    client_secrets = None
    query_url = None

    def __init__(self, credentials_json: str, scopes: list, redirect_uri:str) -> None:
        """
        Creates a :class:`AuthorizationCodeGrantFlow`.

        Args:
            credentials_json (str): The path to the credentials.json
                file.
            scopes (list[str]): The list of scopes to request during the
                API usage.
            redirect_uri (str): The link to redirect the client.
        """
        self.redirec_uri = redirect_uri

        # Verify existence of the credentials file 
        # and if it exists, read the data, else, raise exception
        if os.path.exists(credentials_json):
            with open(credentials_json, 'r') as creds_json:
                creds_data = json.load(creds_json)

            creds_json.close()

            # Verify if got the required keys in the data.
            # Case its True save the values in the variables 
            # and construct the link to the authorization page. 
            # Case its False, raise execption
            if "client_id" in list(creds_data) and "client_secrets" in list(creds_data):

                self.client_id = creds_json["client_id"]
                self.client_secrets = creds_json["client_secrets"]

                # Cronstruct the scopes string                
                _scopes = scopes[0]
                for scope in scopes[1:]:
                    _scopes += "%20" + scope

                self.url = OAUTH2_URL_BASE + oauth_authorize_params.format(self.client_id, redirect_uri, _scopes)

            else:
                raise Exception("Credentials file missing keys")
        else:
            raise FileNotFoundError("Credentials file not found")
       
    def _localServerApp(self, environ, start_response):
        """
        Creat local server app
        """
        status = "200 OK"
        headers = [(
            "Content-type", 
            "text/html; charset=utf-8"
            )]  
        
        start_response(status, headers)

        self.query_url = request_uri(environ)

        return PSEUDO_HTML

    def openLocalServerAuthorization(self) -> str:
        """
        Creat a local server to got the code from teh authorization request
        """
        # Organizar para pegar o url de redirecionamento
        server = make_server("", 500, self._localServerApp)

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

        return r[i:]

    def creatRefreshToken(self, code: str = None, refresh_token: str = None):
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
            data = oauth_new_token_data.format(self.client_id, self.client_secrets, code, self.redirec_uri)

        if refresh_token != None and code == None:
            data = oauth_refresh_token_data.format(refresh_token, self.client_id, self.client_secrets)

        r = requests.post(url, data, headers=OAUTH2_HEADERS)

        # Verify if request succed, case True, verify keys and so on
        # save data in the token.json file
        if r.status_code == 200:
            token_data = r.json()
            if "access_token" in list(token_data) and "refresh_token" in list(token_data) and "token_type" in list(token_data):

                with open("token.json", 'w') as token_json:
                    json.dump(token_data, token_json)
                token_json.close()

                return token_data # return
            
            else:
                raise Exception("Token data missing keys")
            
        else:
            raise Exception("HTTPS response error:\nError getting authorization token")            
        
    def validateToken(self, token):
        """
        Validate the token:
            If token is valid, return client data
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
                raise Exception("Invalid access token")
       
        else:
            raise Exception("HTTPS response error:\n Can't validate token")
        
# testar partes da classe

        





POST_REQUEST = "POST"
GET_REQUEST = "GET"

API_URL_BASE = "https://api.twitch.tv/helix"

CHAT_SCOPE = "/chat/messages" # Não são os scopes
CLIP_SCOPE = "/clips"
USER_SCOPE = "/users"

api_headers_base = {'Authorization': 'Bearer {}','Client-Id': '{}'}

class TwitchClipAPI():
    # Talvez mudar variaveis que se repetem para variaveis self e modificar elas com globais

    def __init__(self, client_id: str, token: str):

        self.headers = api_headers_base["Authorization"].format(token)
        self.headers = api_headers_base["Client-Id"].format(client_id)
    
    def _request(self, request_type: str, url_scope: str, params: dict, headers: str):
        json_data = None

        if request_type == GET_REQUEST:
            r = requests.get(url=API_URL_BASE + url_scope, headers=headers, params=params)
            
        elif request_type == POST_REQUEST:
            r = requests.post(url=API_URL_BASE + url_scope, headers=headers, params=params)
        
        if r.status_code == 200:
            json_data = r.json()['data'][0]
        
        else:
            raise Exception("HTTPS response error")

        return json_data
    
    def UserID(self, username: str):
        request_type = GET_REQUEST
        scope = USER_SCOPE
        params = {
            'login' : username
        }
        headers = self.headers

        data = self._request(request_type, scope, params, headers)
        
        return data['id']
    
    def CreateClip(self, broadcaster_id: str):
        request_type = POST_REQUEST
        scope = CLIP_SCOPE
        params = {
            'broadcaster_id' : broadcaster_id
        }
        headers = self.headers

        data = self._request(request_type, scope, params, headers)
        
        return data['id']
    
    def Clip(self, clip_id: str):
        request_type = GET_REQUEST
        scope = CLIP_SCOPE
        params = {
            'id' : clip_id
        }
        headers = self.headers

        data = self._request(request_type, scope, params, headers)
        
        return data['url']
    
    def ChatMessage(self, broadcaster_id: str, sender_id: str, msg: str):
        request_type = POST_REQUEST
        scope = CHAT_SCOPE
        params = {
            'broadcaster_id' : broadcaster_id,
            'sender_id' : sender_id,
            'message' : msg,
            'for_source_only' : False
        }
        headers = self.headers

        headers['Content-Type'] = 'application/json'

        data = self._request(request_type, scope, params, headers)
        
        return data['is_sent']
    
        
