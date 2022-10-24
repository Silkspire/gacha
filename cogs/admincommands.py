import discord
from discord.ext import commands
import sqlite3
import db

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def clear_all(self, ctx):
        db.clear_all()


def setup(bot):
    bot.add_cog(AdminCommands(bot))