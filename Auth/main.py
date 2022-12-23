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
        "redirect_uri": "https://river-372510.lm.r.appspot.com/callback",
    }
    r = requests.post("https://discord.com/api/oauth2/token", data=data)
    print(f"TOKEN: {r.json()}")
    TOKEN = r.json()['access_token']
    user_data = getUserData(TOKEN)
    updateMetadata(TOKEN, user_data['user']['id'])
    
    print(r)
    return """
        <html>
        <head>
            <title>Verified!</title>
        </head>
        <body onload="window.close();">
            <h1>Successfuly Verified!</h1>
            <h2> You can now close this window.</h2>
            <script>const closeTab = () => window.close(``, `_parent`, ``);
                    closeTab();</script>
        </body>
        </html>"""

@app.route('/verify')
def verify():
    return flask.redirect("https://discord.com/api/oauth2/authorize?client_id=1055370446347968584&redirect_uri=https%3A%2F%2Friver-372510.lm.r.appspot.com%2Fcallback&response_type=code&scope=identify%20guilds%20email%20connections%20role_connections.write")

def getUserData(bearer):
    URL = 'https://discord.com/api/v10/oauth2/@me'
    r = requests.get(URL, headers={"Authorization":f"Bearer {bearer}"})
    return r.json()

def updateMetadata(TOKEN, userid):
    print("Updating metadata")
    meta = {
        "platform_name":"Successfuly Verified!",
        
    } 
    pushMetadata(TOKEN, meta, userid)

def pushMetadata(token, metadata, userid):
    print("Pushing metadata")
    pass
    with open("configs/config.json", "r") as file:
        URL = f"https://discord.com/api/v10/users/@me/applications/1055370446347968584/role-connection"
        data = {    
            "platform_name":"Successfuly Verified!",
            "metadata": metadata,
        }
        headers = {
            "Authorization": f"Bearer {token}", 
            "Content-Type": "application/json"}
        print(f"Headers: {headers}")
        request = requests.put(url=URL, headers=headers, json=data)

        print(request.json())


CLIENT_ID = "1055370446347968584"
CLIENT_SECRET = "wCLOefvgNirx3xsmzuVWEltZNHe3BDzo"   
