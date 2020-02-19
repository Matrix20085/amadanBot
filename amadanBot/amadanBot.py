import ssl
import json
import time
import discord
import asyncio
import requests
import threading
import websockets

from pytz import timezone
from datetime import datetime
from discord.ext import commands
from cryptography.fernet import Fernet as crypt

# Initializing encryption object
keyFile = open("key.key", 'r')
key = str.encode(keyFile.read())
keyFile.close()
cryptObj = crypt(key)
 

# Token Variables
discordToken = cryptObj.decrypt(b"gAAAAABeTU3qWHeMpM55G4d-QaMVCKlZCNgsBOCJ7mLLQGYIdDtrFCEl9pLM5w3AJpjyA2m3zj_D9wpQumBvG2v14ow9NlYqVwqn1L-qo4o6-v25eCGUcbOS0AUcKMBnM6zTcy4mUmOsN6_Nx5CZeUQrQSfu2Kqo4g==").decode('utf8')
dbgToken = cryptObj.decrypt(b"gAAAAABeTVOYxY6bFU4kSSR3H2yxKhoIhhtjpF6WBXKlMCluIFQmptvAniAg1GLc7YMuiW6Lg_pVMFZaOE_LNy6Hjekz48K8ZpaqTcuvhnRvMJDmkNfbGxg=").decode('utf8')

# ID Variables
newRole = int(cryptObj.decrypt(b"gAAAAABeTU3q46ivr76gY5JMzIU56XP7AjOpBQAswXw4SpVbWz39O1dHPQXWkeggZVBs-Cb7RLnuCoHyzbSUz-Of0HCkfcQC1q6uhvGhnhIMvwv7HzOoNmQ=").decode('utf8'))
amadansRole = int(cryptObj.decrypt(b"gAAAAABeTU3qra-bmdsytSUkMdqI1yyqte46X5BhJv5n9HBaxRCfEzGiR0FouSTAI9BMFy3VoPEXMrj9DGtRlWvgDUG_-FtVDoxJnfwzaGi8HePEpstcHjU=").decode('utf8'))
modsRole = int(cryptObj.decrypt(b"gAAAAABeTU3q17cQM0i3rTo7Irj6oU03htCcyFVnvucdKSY0wL5jjYrEp0U9KuyjTTm9ISDNlEMqaVXCQG_au_lueQPopDaXNEO923jV7mTxbYyaWkDnyWc=").decode('utf8'))
entranceChannel = int(cryptObj.decrypt(b"gAAAAABeTU3qZQ1OlbG7ManXAtkXqXmyA4AI0VduWPuKJc7pZ1V3m4QMdV6y_yIszdgbWYX-JnrjbzcWTMdq9NIKHDtqvbR0xjrYC-co9Kf8JH9A3xDInyo=").decode('utf8'))
testChannel = int(cryptObj.decrypt(b"gAAAAABeTU3q8V9cu5baRFxR2cAZOmyOiOrDYaQjZy-COzYL7-yN2qTegzZ1zCXgxG3GCAwaRseQZdx4XX1AMvUqfags29L2B0mK7QIBcXcfiFavYq-j2-s=").decode('utf8'))
botLogChannel = int(cryptObj.decrypt(b"gAAAAABeTU3qzSu2piJf0mwQKlc7oJGQ2tiwxFz2AX-RswA92-bp2eHC6cCVB68-XJ2bZKZvcs8CZy1TveSh8KSeyURJiAOYcLP8LnQMtTgpydrvs4XjJvI=").decode('utf8'))
automatedPingsChannel = int(cryptObj.decrypt(b"gAAAAABeTU3qe6WtGiTIWMPllbgXYiwVIon48H5Ig_abzkx_VanZr0hjIMfrS9QYoEMYvkS6RUE4k0Uvny-WQP4K3ylyifkejsMdoQaHpINblKbO5ywo10c=").decode('utf8'))
botID = int(cryptObj.decrypt(b"gAAAAABeTU3qlKUmfyHIVC4c_L4GjU59Xh6GWMqfhd7DRUmfw-e5ku_A1qQMGtVQmZuCdW-xunuBABfo302eJcs0gS7jh8_OFUfYRxpKQaYWP7URH9GZViw=").decode('utf8'))
serverID = int(cryptObj.decrypt(b"gAAAAABeTU3qHObRALYHQ-TYcoVNJ8qJR9e9qyWGDKJHnX6YN_r1a53r32lFuVuJHPddQYMmwEcHVEHEBGUQmkWawd0kmJ3wgNyTnG3MuKNI5zG8CCk8GPY=").decode('utf8'))


dbgBaseUrl = "https://census.daybreakgames.com/s:" + dbgToken + "/get/ps2:v2/"



client = commands.Bot(command_prefix = '>')


# Fires when bot is connected and ready
@client.event
async def on_ready():
    print("Bot Ready")
    client.loop.create_task(sendMessage("Amadan Bot Ready",botLogChannel))


# Automaticaly adds 'New' on join and sends DM asking for IGN of PS2
@client.event
async def on_member_join(member):
    role = member.guild.get_role(newRole)
    await member.add_roles(role)
    client.loop.create_task(sendMessage(f"Adding 'New' role for {member.display_name}",botLogChannel))
    channel = await member.create_dm()
    await channel.send("Please type you IGN if you are a member of out Planetside 2 outfit. If you do not play Planetside ignore this message.")

# Reads EVERY message it can
@client.event
async def on_message(message):

    # If DM and not from itself
    if (message.guild == None and message.author.id != botID):

        # Requesting and parsing outfit members
        response = requests.get(dbgBaseUrl + "outfit/?name=Amadan&c:resolve=member_character(name)")
        members = response.json()['outfit_list'][0]['members']

        # Getting discord server info since this came from a DM
        server = client.get_guild(serverID)

        # Tracking if member was found
        isMember = False

        # Loop to search through outfit members
        for member in members:
            if member['name']['first_lower'] == message.content.lower():
                isMember = True

                # Getting 'Amadan' object data and adding to member
                role = discord.utils.get(server.roles, id=amadansRole)
                discordMember = server.get_member(message.author.id)
                await discordMember.add_roles(role)
                client.loop.create_task(sendMessage(f"Adding 'Amadan' role for {discordMember.display_name}",botLogChannel))


                # Getting 'New; role object and removing from member
                role = discord.utils.get(server.roles, id=newRole)
                await discordMember.remove_roles(role)


                oldName = discordMember.display_name
                await discordMember.edit(nick=member['name']['first'])
                await message.channel.send("Congratulations, you are now a member in the Discord. Your nickname has been set to your IGN.")
                client.loop.create_task(sendMessage(f"Changing nickname fomr {oldName} to {member['name']['first']}",botLogChannel))
                break

        # If not member send mention to mods in entrance channel
        if not isMember:
            channel = server.get_channel(entranceChannel)
            mods = server.get_role(modsRole)
            await channel.send(f"{message.author.mention} seems to be incapable of spelling thier IGN correctly. Can you help them out {mods.mention}!")
    await client.process_commands(message) # Send the message to see if other commands are embedded 



# List all members with 'New' role
@client.command()
async def listNewMembers(ctx):
    newMembers = ctx.guild.get_role(newRole).members
    await ctx.send(str(len(newMembers)) + " members in the New role.")
    for member in newMembers:
        await ctx.send(member)

# Used for testing
@client.command()
async def ping(ctx):
    await ctx.send("Pong")

# Encrypts string
@client.command()
async def encryptThis(ctx, *, arg):
    client.loop.create_task(sendMessage(cryptObj.encrypt(str.encode(arg)).decode('utf8'),botLogChannel))

# Sends message to testing channel
async def sendMessage(msg, channelID):
    server = client.get_guild(serverID)
    channel = server.get_channel(channelID)
    await channel.send(msg)


# Standing up DBG client 
async def dbgClient():
    endpoint = "wss://push.planetside2.com/streaming?environment=ps2&service-id=s:" + dbgToken
    async with websockets.connect(endpoint, ssl=True) as websocket:
        print("Send subscription string to DBG...")
        client.loop.create_task(sendMessage("Connected to DBG Event Stream",botLogChannel))
        await websocket.send('{"service":"event","action":"subscribe","worlds":["17"],"eventNames":["MetagameEvent"]}')
        # Reciving first message to start the loop
        message = await websocket.recv()
        while message:
            messageJson = json.loads(message)

            # Check if the event is a metagame event
            # Match Event ID to database
            # Check for type = 9, 9 seems to be continent lock alerts
            # http://census.daybreakgames.com/get/ps2:v2/metagame_event?c:limit=1000
            if 'payload' in messageJson:
                eventID = messageJson['payload']['metagame_event_id']
                response = requests.get(dbgBaseUrl + "metagame_event?c:limit=1000")
                ids = response.json()['metagame_event_list']
                for id in ids:
                    if id['metagame_event_id'] == eventID and id['type'] == "9":

                        currentTime = datetime.now(timezone('EST')).strftime("%m-%d %I:%M %p")
                        discordMessage = f"A \"{id['name']['en']}\" alert has {messageJson['payload']['metagame_event_state_name']}! ({currentTime} EST)\n"
                        discordMessage += f"NC: {int(float(messageJson['payload']['faction_nc']))}   TR: {int(float(messageJson['payload']['faction_tr']))}   VS: {int(float(messageJson['payload']['faction_vs']))}\n"
                        discordMessage += "=" * 45

                        client.loop.create_task(sendMessage(discordMessage,automatedPingsChannel))
                        client.loop.create_task(sendMessage(message,botLogChannel))
            message = await websocket.recv()

# Starting Discord Bot
discordBotThread = threading.Thread(target=client.run, args=(discordToken,))
discordBotThread.start()

time.sleep(10)

# Starting DBG Stream 
dbgClientThread = threading.Thread(target=asyncio.run(dbgClient()))
dbgClientThread.start()