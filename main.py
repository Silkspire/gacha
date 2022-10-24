from enum import Enum
from os import X_OK
from pydoc import synopsis
import discord

from discord.ext import commands, pages
from discord.ext.commands.converter import MemberConverter
from discord.ext import tasks
#from discord import Option
import datetime
import requests
import requests_cache
import json
import aiosqlite
import sqlite3
import asyncio
import aiohttp
from statistics import mean
import math
import logging
import os
import atexit
import time
import traceback
import uuid
import db


startup_time = datetime.datetime.now()
intents = discord.Intents.default()
#intents.members = True
#intents.message_content = True
dev=''
try:
    dev = os.environ['dev']
except:
    dev=False
# conn = False
# discord_token = False

try:
    discord_token = db.get_discord_token()
except:
    print("DATABASE COULD NOT BE CONNECTED TO AAAAAAAAAAA")
    quit()



# class MyBot(commands.Bot):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         #self.some_task.start()

#         @tasks.loop(minutes=5)
#         async def some_task(self):
#             await self.wait_until_ready()
#             pass

class MyBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
bot = MyBot()

@bot.event
async def on_ready():
    for guild in bot.guilds:
        print(f"{bot.user} has connected to {guild.name} ({guild.id})")

# @bot.command('uptime')
# async def uptime(ctx):
#     now = datetime.datetime.now()
#     uptime = now - startup_time
#     uptime = uptime - datetime.timedelta(microseconds = uptime.microseconds)
#     print(f"Uptime: {str(uptime)}")
#     await ctx.reply(f"Uptime: {str(uptime)}")

@bot.slash_command(name='uptime', description = "tells the time")
async def uptime(ctx):
    now = datetime.datetime.now()
    uptime = now - startup_time
    uptime = uptime - datetime.timedelta(microseconds = uptime.microseconds)
    print(f"Uptime: {str(uptime)}")
    await ctx.respond(f"Uptime: {str(uptime)}")






#bot.load_extension('cogs.pagetest')
bot.load_extension('cogs.mainmenu')


def close_database():
    db.close_database()
    print("CLOSED DATABASE ON EXIT")
atexit.register(close_database)

bot.run(discord_token)
    # @bot.event
    # async def on_command_error(ctx, error):
    #     # maybe use this more
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.reply(error)
    #     elif isinstance(error, commands.CheckAnyFailure):
    #         await ctx.reply(error)
    #     else:
    #         logger.warning(str(error))

