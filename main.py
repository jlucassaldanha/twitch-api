import os

from twitch_oauth import AuthorizationCodeGrantFlow
from twitch_api import TwitchClipAPI


auth = AuthorizationCodeGrantFlow()


token_file_data = None

if os.path.exists("credentials.json"):
    creds_file = auth.read_credentials_file("credentials.json")
    client_id = creds_file['client_id']
    print("Read Credentials")
else:
    raise Exception("Credentials json file missing")

if os.path.exists("token.json"):
    token_file_data = auth.read_token_file("token.json")
    print("Read Token")

    if not auth.valid_token:
        print("Refresh Token")
        token_file_data = auth.create_refresh_token(refresh_token=token_file_data['refresh_token'])

if not token_file_data:
    print("Create Token")
    code = auth.local_server_authorization()
    
    token_file_data = auth.create_refresh_token(code=code)

token = token_file_data["access_token"]


api = TwitchClipAPI(client_id, token)

user_info = api.users_info(['ojoojao'])
print(user_info[0]["id"])

