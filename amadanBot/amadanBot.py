
#ToDo:
# Create websoket for DGB event streaming
# Parse events
# Send ping to discord with wanted events

import ssl
import json
import time
import discord
import asyncio
import requests
import threading
import websockets
import configparser

from discord.ext import commands

# Private toekns/IDs
configOptions = configparser.ConfigParser()
configOptions.read("amadan.cfg")

# Token Variables
discordToken = configOptions.get('tokens','discord')
dbgToken = configOptions.get('tokens','dbg')

# ID Variables
newRole = int(configOptions.get('discordIDs','newRole'))
amadansRole = int(configOptions.get('discordIDs','amadansRole'))
modsRole = int(configOptions.get('discordIDs','modsRole'))
entranceChannel = int(configOptions.get('discordIDs','entranceChannel'))
testChannel = int(configOptions.get('discordIDs','testChannel'))
botID = int(configOptions.get('discordIDs','botID'))
serverID = int(configOptions.get('discordIDs','serverID'))


dbgBaseUrl = "https://census.daybreakgames.com/s:" + dbgToken + "/get/ps2:v2/"



client = commands.Bot(command_prefix = '>')


# Fires when bot is connected and ready
@client.event
async def on_ready():
    print("Bot Ready")


# Automaticaly adds 'New' on join and sends DM asking for IGN of PS2
@client.event
async def on_member_join(member):
    role = member.guild.get_role(newRole)
    await member.add_roles(role)
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

                # Getting 'New; role object and removing from member
                role = discord.utils.get(server.roles, id=newRole)
                await discordMember.remove_roles(role)


                await discordMember.edit(nick=message.content)
                await message.channel.send("Congratulations, you are now a member in the Discord. Your nickname has been set to your IGN.")
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


# Sends message to testing channel
async def sendMessage(msg):
    server = client.get_guild(serverID)
    channel = server.get_channel(testChannel)
    await channel.send(msg)

# Starting Discord Bot
discordBot = threading.Thread(target=client.run, args=(discordToken,))
discordBot.start()

async def dbgConnect():
    endpoint = "wss://push.planetside2.com/streaming?environment=ps2&service-id=s:" + dbgToken
    async with websockets.connect(endpoint, ssl=True) as websocket:
        print("Send subscription string to DBG...")
        await websocket.send({"service":"event","action":"subscribe","worlds":["17"],"eventNames":["MetagameEvent"]})
        print("String sent.")



async def dbgClient():
    endpoint = "wss://push.planetside2.com/streaming?environment=ps2&service-id=s:" + dbgToken
    async with websockets.connect(endpoint, ssl=True) as websocket:
        #for x in range (0,9):
            #resp = await websocket.recv()
            #print(resp)
        print("Send subscription string to DBG...")
        await websocket.send('{"service":"event","action":"subscribe","worlds":["1","9","10","11","13","17","18","19","25","1000","1001"],"eventNames":["MetagameEvent"]}')
        print("String sent.")
        
        message = await websocket.recv()
        while message:
            messageJson = json.loads(message)

            try:
                #print(messageJson['payload'])
                eventID = messageJson['payload']['metagame_event_id']
                print(eventID)
                response = requests.get(dbgBaseUrl + "metagame_event?c:limit=1000")
                ids = response.json()['metagame_event_list']
                for id in ids:
                    if id['metagame_event_id'] == eventID:
                        print(id['name']['en'])
            except:
                pass
            message = await websocket.recv()


asyncio.get_event_loop().run_until_complete(dbgClient())

print("---Waiting for bot---")
time.sleep(5)
print("---Done waiting---")
task = client.loop.create_task(sendMessage("Yo"))
