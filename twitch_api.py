import requests
import json
import os

# usar biblioteca do google de exemplo

class TwitchOAuth():
    def __init__(self):  
        pass

OAUTH2_HEADERS = {'Content-Type' : 'application/x-www-form-urlencoded'}
OAUTH2_URL_BASE = "https://id.twitch.tv/oauth2"
oauth_authorize_params = "/authorize?response_type=code&client_id={}&redirect_uri={}&scope={}"
oauth_token_data_base = "client_id={}&client_secret={}&code={}&grant_type=authorization_code&redirect_uri={}"

class AuthorizationCodeGrantFlow():
    code = None
    def __init__(self, credentials_json: str, scopes: str, redirect_uri:str):
        self.redirec_uri = redirect_uri

        if os.path.exists(credentials_json):
            with open(credentials_json, 'r') as creds_json:
                creds_data = json.load(creds_json)

            creds_json.close()

            if "client_id" in list(creds_data) and "client_secrets" in list(creds_data):

                self.client_id = creds_json["client_id"]
                self.client_secrets = creds_json["client_secrets"]

                self.url = OAUTH2_URL_BASE + oauth_authorize_params.format(self.client_id, redirect_uri, scopes)

            else:
                raise Exception("Credentials file missing keys")
        else:
            raise FileNotFoundError("Credentials file not found")
        
    def openAuthorization(self):
        # Faz todo o negocio do servidor
        # Response: http://localhost:3000/?code=gulfwdmys5lsm6qyz4xiz9q32l10&scope=channel%3Amanage%3Apolls+channel%3Aread%3Apolls&state=c3ab8aa609ea11e793ae92361f002671

        # http://localhost:3000/?error=access_denied&error_description=The+user+denied+you+access&state=c3ab8aa609ea11e793ae92361f002671
        pass

    def token(self):
        url = OAUTH2_URL_BASE + "/token"
        data = oauth_token_data_base.format(self.client_id, self.client_secrets, self.code, self.redirec_uri)

        r = requests.post(url, data, headers=OAUTH2_HEADERS)

        if r.status_code == 200:
            token_data = r.json()

            with open("token.json", 'w') as token_json:
                json.dump(token_data, token_json)
            token_json.close()

            return token_data

        else:
            raise Exception("HTTPS response error")
        
    def refreshToken(self):
        pass


        
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
    
        
