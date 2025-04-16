import requests as req
import webbrowser as webb
import json


class pySimpleTwitch():

    def auth(self, client_id: str, scopes: list, redirect: str):
        
        _scopes = scopes[0]
        for scope in scopes[1:]:
            _scopes += "%20" + scope

        auth_url = f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect}&scope={_scopes}"

        webb.open(auth_url)

    def auth_token(self, client_id: str, client_secret: str, code: str, redirect: str):

        token_url = "https://id.twitch.tv/oauth2/token"

        headers = {'Content-Type':'application/x-www-form-urlencoded'}

        data = f"client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={redirect}"

        response = req.post(token_url, data, headers=headers)

        json_data = response.json()
        # Adiciona no json a data

        with open("credentials.json", 'w') as json_file:
            json.dump(json_data, json_file)

        json_file.close()

    def authentication(self, json_file: str):
        # Faz a leitura do json e pega os valores, ve a data
        return 0
    
    def refresh_authentication(self, refresh_token: str, client_id: str, client_secret: str):
        token_url = "https://id.twitch.tv/oauth2/token"

        headers = {'Content-Type':'application/x-www-form-urlencoded'}

        data = f"grant_type=refresh_token&refresh_token={refresh_token}&client_id={client_id}&client_secret={client_secret}"

        response = req.post(token_url, data, headers=headers)

        json_data = response.json()
        # Adiciona no json a data

        with open("credentials.json", 'w') as json_file: 
            json.dump(json_data, json_file)

        json_file.close()

    def get_userID(self, client_id: str, token: str, username: str):
        url = "https://api.twitch.tv/helix/users"

        params = {'login':username}

        headers = {'Authorization': f'Bearer {token}','Client-Id': client_id}

        response = req.get(url, params=params, headers=headers)

        json_response = response.json()

        user_id = json_response["data"][0]["id"]

        return user_id
    
    def creat_clip(self, client_id: str, token: str, user_id: str):
        url = 'https://api.twitch.tv/helix/clips'

        params = {'broadcaster_id' : user_id}
        
        headers = {'Authorization': f'Bearer {token}','Client-Id': client_id}

        response = req.post(url, params=params, headers=headers)

        json_response = response.json()

        clip_id = json_response["data"][0]["id"]
        clip_url = json_response["data"][0]["edit_url"]

        return clip_id, clip_url
    
    def clip_verify(self, client_id: str, token: str, clip_id: str):

        url = 'https://api.twitch.tv/helix/clips'

        headers = {'Authorization': f'Bearer {token}','Client-Id': client_id}

        params = {'id':clip_id}

        response = req.get(url, params=params, headers=headers)

        clip_url = ""

        if response == 200:
            json_response = response.json()

            _clip_id = json_response["data"][0]["id"]

            if _clip_id == clip_id:
                clip_url = json_response["data"][0]["url"]

        return clip_url
    
    def chat_msg(self, client_id: str, token: str, user_id:str, msg: str):

        url = 'https://api.twitch.tv/helix/chat/messages'

        headers = {'Authorization': f'Bearer {token}','Client-Id': client_id, 'Content-Type': 'application/json'}

        data = {
            "broadcaster_id": user_id,
            "sender_id": user_id,
            "message": "Hello, world! twitchdevHype",
            "for_source_only": False
            }
        
        response = req.post(url, params=data, headers=headers)

        json_response = response.json()

    







