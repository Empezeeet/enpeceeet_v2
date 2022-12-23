import flask
import requests

app = flask.Flask(__name__)

@app.route("/")
def default():
    return flask.redirect("https://discord.com/api/oauth2/authorize?client_id=1055370446347968584&permissions=2483030032&redirect_uri=https%3A%2F%2Friver-372510.lm.r.appspot.com%2Fcallback&response_type=code&scope=identify%20email%20connections%20bot%20role_connections.write")

@app.route("/invite")
def invite():
    return flask.redirect("https://discord.com/api/oauth2/authorize?client_id=1055370446347968584&permissions=2483030032&redirect_uri=https%3A%2F%2Friver-372510.lm.r.appspot.com%2Fcallback&response_type=code&scope=identify%20email%20connections%20bot%20role_connections.write")


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
            <style>
                body {
                    font-family: Arial, Helvetica, sans-serif;
                    background-color: #282428;
                    color: #a1a1a1
                }
                .center {
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                    width: 50%;
                    text-align: center;
                    
                }
                
                .widget {
                    margin-left: 33%;
                    width: 33%;
                    scale: 90%;
                }
            </style>
        </head>
        <body onload="">
            <h1 id="h1" class="center" >Successfuly Verified!</h1>
            <h2 id="h2" class="center"> You can now close this window.</h2>
            <h3 id="thanks" class="center">Thank you for using RiverBot!</h3>
            <h3 id="server" class="center">Support Server:</h3>
            <iframe class="widget" src="https://discord.com/widget?id=1055813218653700166&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
            
            
            
            <script>
            const closeTab = () => window.close(``, `_parent`, ``);
            closeTab();
            var lang = navigator.language || navigator.userLanguage;
            if (lang.includes("pl")) {
                docuemnt.getElementById("h1").innerHTML = "Pomyślnie zweryfikowano!";
                document.getElementById("h2").innerHTML = "Możesz teraz zamknąć to okno.";
                document.getElementById("thanks").innerHTML = "Dziękujemy za korzystanie z RiverBot!";
                document.getElementById("server").innerHTML = "Support:";
                
            } else if (lang.includes("de")) {
                docuemnt.getElementById("h1").innerHTML = "Erfolgreich verifiziert!";
                document.getElementById("h2").innerHTML = "Sie können dieses Fenster nun schließen.";
                document.getElementById("thanks").innerHTML = "Vielen Dank für die Nutzung von RiverBot!";
                document.getElementById("server").innerHTML = "Support:";
            }
            
            
            
            
            </script>
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
