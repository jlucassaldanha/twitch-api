import requests

# Arrumar esse codigo na parte dos escopos para que não fique tão fechado assim

API_URL_BASE = "https://api.twitch.tv/helix"

CHAT_SCOPE = "/chat/messages" # Não são os scopes
CLIP_SCOPE = "/clips"
USER_SCOPE = "/users"

class TwitchClipAPI():
    # Talvez mudar variaveis que se repetem para variaveis self e modificar elas com globais

    def __init__(self, client_id: str, token: str):

        self.headers = {
            'Authorization': f'Bearer {token}',
            'Client-Id': client_id}
    
    def UsersID(self, usernames: list = None, ids: list = None):
        
        if usernames != None and len(usernames) <= 100:
            url_data = "?login="+usernames[0]
            if len(usernames) > 1:
                for username in usernames[1:]:
                    url_data += "&login="+username

        if ids != None and len(ids) <= 100:
            url_data = "?id="+ids[0]    
            if len(ids) > 1:
                for id in ids[1:]:
                    url_data += "&id="+id

        if usernames != None and ids != None:
            if len(usernames) <= 50 and len(ids) <= 50:
                url_data = "?login="+usernames[0]
                if len(usernames) > 1:
                    for username in usernames[1:]:
                        url_data += "&login="+username
                
                url_data += "&id="+ids[0]
                if len(ids) > 1:
                    for id in ids[1:]:
                        url_data += "&id="+id

        url = API_URL_BASE + USER_SCOPE + url_data

        r = requests.get(url=url, headers=self.headers)

        if r.status_code == 200:
            self.user_data = r.json()

            return self.user_data['data']
        
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
        
        elif r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")
    
    def CreateClip(self, broadcaster_id: str, has_delay: bool = False):
        url = API_URL_BASE + CLIP_SCOPE

        params = {
            'broadcaster_id' : broadcaster_id,
            'has_delay' : has_delay
        }

        r = requests.post(url, params=params, headers=self.headers)

        if r.status_code == 202:
            self.created_clip_data = r.json()

            return self.created_clip_data['data'][0]
        
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
        if r.status_code == 403:
            raise Exception("HTTPS response error:\n Can't make clips of this broadcaster")
        if r.status_code == 404:
            raise Exception("HTTPS response error:\n Broadcaster must be in live")
    
    def getClip(self, clip_id: str):
        # Da para melhorar depois igual o de users, mas são muitos parametros, então vou com calma
        url = API_URL_BASE + CLIP_SCOPE
        params = {
            'id' : clip_id
        }

        r = requests.get(url, params=params, headers=self.headers)
        
        if r.status_code == 200:
            self.clip_data = r.json()

            return self.clip_data['data']
                
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
        elif r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")
    
    def ChatMessage(self, broadcaster_id: str, sender_id: str, msg: str):
        url = API_URL_BASE + CHAT_SCOPE
        
        params = {
            'broadcaster_id' : broadcaster_id,
            'sender_id' : sender_id,
            'message' : msg
        }

        headers = self.headers
        headers['Content-Type'] = 'application/json'

        r = requests.post(url, params=params, headers=headers)
        
        if r.status_code == 200:
            self.chat_message_data = r.json()

            return self.chat_message_data['data']
                
        if r.status_code == 401:
            raise Exception("HTTPS response error:\n Invalid access token, client id or scopes")
        if r.status_code == 400:
            raise Exception("HTTPS response error:\n Bad request with wrong parameters")
        if r.status_code == 403:
            raise Exception("HTTPS response error:\n Can't send chat messages to this broadcaster")
        if r.status_code == 422:
            raise Exception("HTTPS response error:\n Message too large to send")
        
    
# Checklist das funções:
# __init__ - OK
# UsersID - OK
# CreateClip - OK
# getClip - OK (melhorar)
# ChatMessage - OK (melhorar)


    
        
