import discord
from discord.ext import commands
import sqlite3

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot