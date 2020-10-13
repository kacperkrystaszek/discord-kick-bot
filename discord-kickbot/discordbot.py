import discord

import json

from discord.ext import commands

import os

import boto3

import asyncio

client = commands.Bot(command_prefix="&") #you can change prefix which runs command

GUILD = 'your guild name' #enter your guild name

BUCKET = os.environ.get('S3_BUCKET_NAME')

#this part manages on amazon s3

def uploading(bucket):
    s3 = boto3.client('s3')
    s3.upload_file('ranking.json',bucket,'ranking.json')

def downloading(bucket):
    s3 = boto3.client('s3')
    s3.download_file(bucket,"ranking.json",'ranking.json')

downloading(BUCKET)

#shows if bot works properly, you can see it on console log

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            print("gotowy")

#events like deafen user, muted user or moved to afk channel

@client.event
async def on_voice_state_update(member, before, after):
    channel = client.get_channel('your text channel id')
    if after.afk:
        await member.move_to(channel = None, reason = None)
        await channel.send(f'your {member.mention} message')
        with open('ranking.json','r') as f:
            ranking = json.load(f)
        if str(member.id) in ranking:
            ranking[str(member.id)]+=1
        else:
            ranking[str(member.id)]=1
        with open('ranking.json','w') as f:
            json.dump(ranking,f)
        
    elif member.voice.self_deaf:
        bot = False
        for role in member.roles:
            if role.id == 'bot role id on your guild':
                bot = True
            else:
                continue
        if bot:
            pass
        else:
            await asyncio.sleep(910)
            if member.voice.self_deaf:
                await member.move_to(channel = None, reason = None)
                await channel.send(f'your {member.mention} message')
                with open('ranking.json','r') as f:
                    ranking = json.load(f)
                if str(member.id) in ranking:
                    ranking[str(member.id)]+=1
                else:
                    ranking[str(member.id)]=1
                with open('ranking.json','w') as f:
                    json.dump(ranking,f)

    elif member.voice.self_mute:
        bot = False
        for role in member.roles:
            if role.id == 'bot role id on your guild':
                bot = True
            else:
                continue
        if bot:
            pass
        else:
            await asyncio.sleep(910)
            if member.voice.self_mute:
                await member.move_to(channel=None,reason = None)
                await channel.send(f'your {member.mention} message')
                with open('ranking.json','r') as f:
                    ranking = json.load(f)
                if str(member.id) in ranking:
                    ranking[str(member.id)]+=1
                else:
                    ranking[str(member.id)]=1
                with open('ranking.json','w') as f:
                    json.dump(ranking,f)

    uploading(BUCKET)

#commands

@client.command()

async def ranking(ctx):
    channel = client.get_channel('your text channel id')
    place = 1
    with open('ranking.json','r') as f:
        ranking = json.load(f)
    sortedRank = {k: v for k, v in sorted(ranking.items(), key=lambda item: item[1],reverse=True)}
    if len(sortedRank) == 0:
        await channel.send("Rank is empty")
    else:
        for userId in sortedRank:
            for guild in client.guilds:
                if guild == 'your guild name':
                    myGuild = guild
            user = myGuild.get_member(int(userId))
            if user == None:
                pass
            else:
                string += str(place) + ". "+str(user.mention)+" - "+str(sortedRank[userId])+" times kicked\n"
                place += 1
        await channel.send(string)

client.run('your token here')