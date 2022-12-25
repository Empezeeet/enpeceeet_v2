import time
import requests
import json
import datetime
from termcolor import colored
import console.utils as utils
import socket
import threading
from colorama import just_fix_windows_console
import modules.command_handlers as ch
# OWN MODULES
import modules.gateway_handler as gh



# Change Activity settings in config.json
start_time = time.time()
just_fix_windows_console()
handler = None
with open("configs/config.json", "r") as config:
    loaded = json.loads(config.read())
    TOKEN = loaded["bot"]["token"]
    APPID = loaded["bot"]["id"]
    AUTH_HEADER = {"Authorization": "Bot " + TOKEN}
    ACTIVITY = loaded["activity"]
    VERSION = loaded['version']
    
    handler = gh.GatewayHandler(TOKEN, APPID, ACTIVITY, VERSION, True)
    
    utils.set_title(f"{loaded['name']} v{VERSION} | Gateway Handler by Empezeeet#8540")








ready_event = handler.receive_json_response(handler.ws)
if (ready_event) and ready_event['t'] == "READY":
    handler.logger.log("MAIN", "Connected to Discord API.")
    handler.logger.log(
        "MAIN", 
        f"""
        Connection Info:\n
        \tAPI Version: {ready_event['d']['v']}
        \tSessionID: {ready_event['d']['session_id']}
        \t{colored("See more info in rundata.json", attrs=["reverse"])}\n"""
    )
    # Set commands
    
    with open("configs/rundata.json", "w") as file:
        r = requests.get(f"https://discord.com/api/v10/applications/{APPID}/commands", headers=AUTH_HEADER).json()
        commands = [cmd['id'] for cmd in r]
        
        data = {
            "time": str(datetime.datetime.now()),
            "start_timestamp": start_time,
            "api_version": ready_event['d']['v'],
            "app_version": VERSION,
            "session_id": ready_event['d']['session_id'],
            "heartbeat_interval": handler.hb_interval,
            "user": ready_event['d']['user'],
            "resume_gateway_url": ready_event['d']['resume_gateway_url'],
            "guilds": ready_event['d']['guilds'],
            "commands":commands
        }
        
        file.write(json.dumps(data, indent=4))
        handler.connected = True
    #handler.setup_commands2()
    handler.force_create_commands()

try:
        
    if __name__ == "__main__":
        # Inform user that initialization is complete
        handler.logger.log("MAIN", colored(f"Initialization completed. ({round(time.time() - start_time, 4)})", "green"))
        handler.logger.log("MAIN", "Starting event loop...")
        
        
        
        
        
        while True:
            
            recv = handler.receive_json_response(handler.ws)
            if not recv: continue # If Recv is nothing just continue.
            #try:
            handler.last_sequence = recv['s']
            handler.logger.log("MAIN", f"Event Received: {recv['t']}")
            if recv['t'] == "INTERACTION_CREATE":
                print(recv)
                if "name" in recv['d']['data'].keys() and recv['d']['data']['name'] == "setup": 
                    ch.handleSetup(recv, handler)
                    continue
                if "token" in recv['d']:
                    ch.handleLangChange(recv, handler, )
                    continue
                    
                
                
                      
                
                
                # Check if user has permissions to use this command
                
                
                
            #except KeyError as e:
            #    handler.logger.log(colored("ERROR", "red"), f"TypeError[main]: {e}")
            
            
            
except KeyboardInterrupt:
    handler.logger.log("MAIN", "User Interrupted program with Ctrl+C. Safe Exit initiated...")
    handler.closeConnection()
    exit()

