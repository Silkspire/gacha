import discord
from discord.ext import commands
import sqlite3
import db

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def reset(self, ctx):
        db.reset()
        await ctx.respond('Databae cleared!')


def setup(bot):
    bot.add_cog(AdminCommands(bot))