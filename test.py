from enum import Enum
from os import X_OK
from pydoc import synopsis
import discord
from discord.ext import commands
from discord.ext.commands.converter import MemberConverter
from discord.ext import tasks
#from discord import Option
import datetime
import requests
import requests_cache
import json
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

def init():
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    dev=''
    try:
        dev = os.environ['dev']
    except:
        dev=False
    prefix = '!'

    bot = MyBot(command_prefix=prefix, intents=intents)

def command_init():
    @bot.event
    async def on_ready():
        for guild in bot.guilds:
            print(f"{bot.user} has connected to {guild.name} ({guild.id})")

    @bot.command('uptime')
    async def uptime(ctx):
        now = datetime.datetime.now()
        uptime = now - startup_time
        uptime = uptime - datetime.timedelta(microseconds = uptime.microseconds)
        logger.info('this is a test')
        await ctx.reply(f"Uptime: {str(uptime)}")
    
    # @bot.event
    # async def on_command_error(ctx, error):
    #     # maybe use this more
    #     if isinstance(error, commands.CommandOnCooldown):
    #         await ctx.reply(error)
    #     elif isinstance(error, commands.CheckAnyFailure):
    #         await ctx.reply(error)
    #     else:
    #         logger.warning(str(error))


class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.some_task.start()

        @tasks.loop(minutes=5)
        async def some_task(self):
            await self.wait_until_ready()
            pass