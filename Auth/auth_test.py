import flask
import json
import requests
import time

app = flask.Flask(__name__)

@app.route("/callback")
def callback():
    code = flask.request.args.get("code")
    data = {
        "client_id": "1055370446347968584",
        "client_secret": "wCLOefvgNirx3xsmzuVWEltZNHe3BDzo",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:8080/callback",
    }
    r = requests.post("https://discord.com/api/oauth2/token", data=data)
    print(f"TOKEN: {r.json()}")
    TOKEN = r.json()['access_token']
    user_data = getUserData(TOKEN)
    with open("configs/tokens.json", "r+") as tokenFile:
        fdata = json.load(tokenFile)
        fdata[user_data['user']['id']] = {
            "expires": time.time() + r.json()['expires_in'],
            "token": TOKEN,
            "refresh_token": r.json()['refresh_token']
        }
        tokenFile.seek(0)
        json.dump(fdata, tokenFile, indent=4)
    updateMetadata(user_data['user']['id'])
    
    print(r)
    return """YOU DID IT! Thank you for verifying with RiverBot!"""

@app.route('/verify')
def verify():
    return flask.redirect("https://discord.com/api/oauth2/authorize?client_id=1055370446347968584&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fcallback&response_type=code&scope=identify%20email%20guilds%20role_connections.write%20connections")

def getUserData(bearer):
    URL = 'https://discord.com/api/v10/oauth2/@me'
    r = requests.get(URL, headers={"Authorization":f"Bearer {bearer}"})
    return r.json()

def updateMetadata(userid):
    print("Updating metadata")
    TOKEN = getAccessToken(userid)
    # hehe
    meta = {
        "cooked": "true",
        "how_much": "a lot"
    } 
    pushMetadata(TOKEN, meta, userid)

def pushMetadata(token, metadata, userid):
    print("Pushing metadata")
    pass
    with open("configs/config.json", "r") as file:
        URL = f"https://discord.com/api/v10/users/@me/applications/1055370446347968584/role-connection"
        ACCESS_TOKEN = getAccessToken(userid)
        data = {    
            "metadata": metadata,
        }
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}", 
            "Content-Type": "application/json"}
        print(f"Headers: {headers}")
        request = requests.put(url=URL, headers=headers, json=data)

        print(request.json())

    
    
def getAccessToken(userid):
    with open("configs/tokens.json", "r") as file:
        file = json.load(file)
        if (time.time() > file[userid]['expires']):
            # Get new token
            print("REFRESHING TOKEN")
            data = {
                'refresh_token': file[userid]['refresh_token'],
                'grant_type': 'refresh_token'
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            r = requests.post('https://discord.com/api/v10/oauth2/token', data=data, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))
            request = r.json()
            print(f"REQUEST2: {request}")
            file[userid]['expires'] = request['expires_in'] + time.time()
            file[userid]['token'] = request['access_token']
            file[userid]['refresh_token'] = request['refresh_token']
            return request['access_token']
        else:
            print(f"RETURNING: {file[userid]['token']}")
            return file[userid]['token']
        
        

if __name__ == "__main__":
    with open("configs/config.json", "r") as config:
        config = json.load(config)
        global CLIENT_ID, CLIENT_SECRET
        CLIENT_ID = config['bot']['id']
        CLIENT_SECRET = config['bot']['client_secret']
    app.run(port=8080)