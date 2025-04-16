import requests
import json
import os

# usar biblioteca do google de exemplo

class TwitchOAuth():
    def __init__(self):
        pass
    

        

POST_REQUEST = "POST"
GET_REQUEST = "GET"

CHAT_SCOPE = "/chat/messages"
CLIP_SCOPE = "/clips"
USER_SCOPE = "/users"

class TwitchClipAPI():
    url_base = "https://api.twitch.tv/helix"
    headers_base = {'Authorization': 'Bearer {}','Client-Id': '{}'}

    def __init__(self, client_id: str, token: str):

        self.headers_base["Authorization"].format(token)
        self.headers_base["Client-Id"].format(client_id)
    
    def _request(self, request_type: str, url_scope: str, params: dict, headers: str):
        json_data = None

        if request_type == GET_REQUEST:
            r = requests.get(url=self.url_base + url_scope, headers=headers, params=params)
            
        elif request_type == POST_REQUEST:
            r = requests.post(url=self.url_base + url_scope, headers=headers, params=params)
        
        if r.status_code == 200:
            json_data = r.json()['data'][0]

        return json_data
    
    def UserID(self, username: str):
        request_type = GET_REQUEST
        scope = USER_SCOPE
        params = {
            'login' : username
        }
        headers = self.headers_base

        data = self._request(request_type, scope, params, headers)
        
        return data['id']
    
    def CreateClip(self, broadcaster_id: str):
        request_type = POST_REQUEST
        scope = CLIP_SCOPE
        params = {
            'broadcaster_id' : broadcaster_id
        }
        headers = self.headers_base

        data = self._request(request_type, scope, params, headers)
        
        return data['id']
    
    def Clip(self, clip_id: str):
        request_type = GET_REQUEST
        scope = CLIP_SCOPE
        params = {
            'id' : clip_id
        }
        headers = self.headers_base

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
        headers = self.headers_base

        headers['Content-Type'] = 'application/json'

        data = self._request(request_type, scope, params, headers)
        
        return data['is_sent']
    
    

        

