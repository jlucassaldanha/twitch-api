import requests
import json
import os

# usar biblioteca do google de exemplo

class TwitchOAuth():
    def __init__(self, credentials_json: str, scopes: list):

        if os.path.exists("token.json"):
            self.token_data = self._read_token("token.json")
        

        pass

    def _read_token(self, filename: str):
        with open(filename, 'r') as token_json:
            data = json.load(token_json)
        token_json.close()

        self.token = 1
        return data
    

        
POST_REQUEST = "POST"
GET_REQUEST = "GET"

URL_BASE = "https://api.twitch.tv/helix"

CHAT_SCOPE = "/chat/messages" # Não são os scopes
CLIP_SCOPE = "/clips"
USER_SCOPE = "/users"

headers_base = {'Authorization': 'Bearer {}','Client-Id': '{}'}

class TwitchClipAPI():
    # Talvez mudar variaveis que se repetem para variaveis self e modificar elas com globais

    def __init__(self, client_id: str, token: str):

        self.headers = headers_base["Authorization"].format(token)
        self.headers = headers_base["Client-Id"].format(client_id)
    
    def _request(self, request_type: str, url_scope: str, params: dict, headers: str):
        json_data = None

        if request_type == GET_REQUEST:
            r = requests.get(url=URL_BASE + url_scope, headers=headers, params=params)
            
        elif request_type == POST_REQUEST:
            r = requests.post(url=URL_BASE + url_scope, headers=headers, params=params)
        
        if r.status_code == 200:
            json_data = r.json()['data'][0]

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
    
        
