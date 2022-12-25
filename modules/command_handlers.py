import requests
import time
import json
with open("configs/config.json", "r") as config:
    global TOKEN, APPID, AUTH_HEADER
    loaded = json.loads(config.read())
    TOKEN = loaded["bot"]["token"]
    APPID = loaded["bot"]["id"]
    AUTH_HEADER = {"Authorization": "Bot " + TOKEN}



def handleSetup(recv, handler):
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
        if guild_lang not in ["en-US", "en-GB", "pl", "de"]: guild_lang = "en-US"
        elif guild_lang == "en-GB": guild_lang = "en-US"
        
    else: guild_lang = DATA[2]
        
    handler.logger.log("MAIN", f"DATA: {DATA}")

    message = ""
    with open("configs/messages.json", "r") as file:
        messages = json.loads(file.read())
        messages = messages[guild_lang]
        message = generateTutorialEmbed(messages=messages, verifiedRoleID=DATA[1])
        
    

    msgreq = requests.post(
        url=f"https://discord.com/api/v10/channels/{DATA[0]}/messages",
        headers={"Authorization": f"Bot {TOKEN}", "Content-Type": "application/json"},
        json={
            "embeds":[message],
            "components": [
                {
                    "type": 1,
                    "components": [
                        {
                            "type": 3,
                            "custom_id":"verify_lang_selection",
                            "options": [
                                {
                                    "label": "English",
                                    "value": "en-US",
                                    "description": "English version of the tutorial",
                                },
                                {
                                    "label": "Polski",
                                    "value": "pl",
                                    "description": "Polska wersja tutoriala",
                                
                                },
                                {
                                    "label": "Deutsch",
                                    "value": "de",
                                    "description": "Deutsche Version des Tutorials",
                                    
                                }
                            ],
                            "placeholder": messages[11],
                            "min_values": 1,
                            "max_values": 1
                        }
                    
                    ]
                }
            ]
    
        }
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
    return DATA

def handleLangChange(recv, handler, verifiedRoleID):
    responseURL = f"https://discord.com/api/v10/interactions/{recv['d']['id']}/{recv['d']['token']}/callback"
    with open("configs/messages.json", "r") as file:
        messages = json.loads(file.read())[recv['d']['data']['values'][0]]
        message = generateTutorialEmbed(messages=messages, verifiedRoleID=verifiedRoleID)
    payload = {
        "type":4,
        "data":{
            "embeds":[message]
        }
    }
    r = requests.post(responseURL, payload)
    handler.logger.log("MAIN", f"Sent message ({r.status_code})")


def generateTutorialEmbed(messages, verifiedRoleID):
        return {
            "title": messages[0],
            "type": "rich",
            "fields":[
                {
                    "title":messages[6],
                    "value":messages[1],
                    "name":messages[6],
                },
                {
                    "title":messages[7],
                    "value":messages[2],
                    "name":messages[7]
                },
                {
                    "title":messages[8],
                    "value":f"{messages[3]}<@&{verifiedRoleID}>",
                    "name":messages[8]
                },
                {
                    "title":messages[9],
                    "value":messages[4],
                    "name":messages[9]
                },
                {
                    "title":messages[10],
                    "value":messages[5],
                    "name":messages[10]
                }
            ],
            "author": {
                "name": "RiverBot",
                "url":"https://river-372510.lm.r.appspot.com/invite",
                "icon_url":"https://cdn.discordapp.com/avatars/1055370446347968584/763c7aaf07d2fb7134b71d53928e7914.png"
            }                        
        }   