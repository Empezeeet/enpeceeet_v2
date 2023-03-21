try: 
    import time
    import modules.logging as logger
    import websocket
    import threading
    import requests
    import json
    import datetime
    import random
    from termcolor import colored
except ModuleNotFoundError as err:
    print(f"MODULE NOT FOUND: {err}")
    exit()
start_time = time.time()


class GatewayHandler(threading.Thread):
    def __init__(self, **kwargs):
        """
            ARGS:
                > token: str - Your Discord Bot's Token
                > appID: str - Your Discord Bot's Application ID
                > activity: dictionary - Your Discord Bot's Activity (See documentation for formatting info)
                > version: str - Your Discord Bot's Version
                > name: str - Your Discord Bot's Name
                
        """
        # User-set variables
        self.token = kwargs.get("token", None)
        self.appID = kwargs.get("appID", None)
        self.activity = kwargs.get("activity", None)
        self.version = kwargs.get("version", None)
        self.name = kwargs.get("name", None)
        if (not self.token or not self.appID or not self.activity or not self.version or not self.name):
            raise Exception("Missing required arguments")
        
        # Internal variables
        self.last_response = None
        self.last_sequence = None
        self.auth_header = {"Authorization": f"Bot {self.token}"} # Authorization header for requests
        self.heartbeat_interval = None # Heartbeat interval in milliseconds
        self.active_commands = []
    
        # Objects
        self.logger = logger.logging.Logger(f"logs/log", self.name, self.version)
        self.ws = websocket.WebSocket()
        
        # Initialization
        self.logger.log("GATEWAY", "Initializing...")
        self.ws.connect('wss://gateway.discord.gg/?v=6&encording=json')      
            # Receive hello event
        hello = self.recv_json(self.ws)
        
          
        identifyJSON = {
            "op": 2,
            "d": {
                "token": self.TOKEN,
                "intents": 513,
                "properties": {
                    "os": "linux",
                    "browser": "Safari",
                    "device": "BDB"
                },
                "presence": {
                    "since": start_time,
                    "activities": [{
                        "name": self.activity["name"],
                        "type": self.activity["type"],
                        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                    }],
                    "status": "online",
                    "afk": False
                }
            },
            "s": self.last_sequence,
            "t": None
        }
        self.send_json(self.ws, identifyJSON)
        # Start heartbeating
        self
        
        
        
        
        pass

    def recv_json(self, ws):
        response = None
        try:
            response = ws.recv()
        except:
            self.logger.log("GATEWAY", "Connection closed by server")
            self.logger.log("GATEWAY", "Reconnecting...")
            # reconnect
    
    def send_json(self, ws, request):
        ws.send(json.dumps(request))
        pass