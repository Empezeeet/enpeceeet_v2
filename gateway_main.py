import time
import requests
import json
import datetime
from termcolor import colored
import console.utils as utils
import socket
import threading
from colorama import just_fix_windows_console

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
            handler.logger.log("MAIN", "Waiting for event...")
            
            recv = handler.receive_json_response(handler.ws)
            if not recv: continue # If Recv is nothing just continue.9
            print(f"RECEIVED: {recv}\n\n")
            try:
                handler.last_sequence = recv['s']
                handler.logger.log("MAIN", f"Event Received: {recv['t']}")
                if recv['t'] != "INTERACTION_CREATE": continue
                if recv['d']['data']['name'] != "setup": continue   
                
                      
                
                
                
                
                if len(recv['d']['data']['options']) > 2:
                    handler.logger.log("MAIN", "SPECIFIED LANG")
                    # ChannelID, RoleID, Language
                    DATA = (
                        recv['d']['data']['options'][0]['value'],
                        recv['d']['data']['options'][1]['value'],
                        recv['d']['data']['options'][2]['value'],
                    )
                
                
                else:
                    handler.logger.log("MAIN", "NO LANG SPECIFIED")
                    DATA = (
                            recv['d']['data']['options'][0]['value'],
                            recv['d']['data']['options'][1]['value'],
                            False,
                        )
                if DATA[2] == False:
                    # NO LANG SPECIFIED
                    # USE GUILD LANG
                    # IF GUILD LANG IS NOT (en-XX, pl, de) use en-US
                    guild_lang = recv['d']['guild_locale']
                    if guild_lang not in ["en-US", "en-GB", "pl", "de"]:
                        guild_lang = "en-US"
                        
                    if guild_lang == "en-GB": guild_lang = "en-US"
                else:
                    guild_lang = DATA[2]
                handler.logger.log("MAIN", f"DATA: {DATA}")

                message = ""
                with open("configs/messages.json", "r") as file:
                    messages = json.loads(file.read())
                    messages = messages[guild_lang]
                    message = f"{messages[0]}\n{messages[1]}\n{messages[2]}\n{messages[3]}<@&{DATA[1]}>\n{messages[4]}\n{messages[5]}\n"
                
                

                msgreq = requests.post(
                    url=f"https://discord.com/api/v10/channels/{DATA[0]}/messages",
                    headers={"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"},
                    json={"content":message}
                )
                
                handler.logger.log("MAIN", f"Sent message ({msgreq.status_code})")
                handler.logger.log("MAIN", msgreq.json())
                
                #handler.logger.log('MAIN', "STATUS: " + str(req.status_code))
                # Set up bot.
                req = requests.post(
                    f"https://discord.com/api/v10/interactions/{recv['d']['id']}/{recv['d']['token']}/callback",
                    json={"type": 4,"data": {"content": "Successfully set up the bot!"}},
                    headers={"Content-Type": "application/json"}
                )
                handler.logger.log("MAIN", f"SET up the bot! ({req.status_code})")
                
            except KeyError as e:
                handler.logger.log(colored("ERROR", "red"), f"TypeError[main]: {e}")
            
            
            
except KeyboardInterrupt:
    handler.logger.log("MAIN", "User Interrupted program with Ctrl+C. Safe Exit initiated...")
    handler.closeConnection()
    exit()

