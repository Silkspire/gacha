import discord
from discord.ext import commands
import sqlite3
import db

from classes.BaseCharacter import *
from classes.Enemy import *
from classes.GameState import *
from classes.InstantiatedCharacter import *
from classes.Monster import *
from classes.Player import *
from classes.User import *

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command()
    async def reset(self, ctx):
        db.reset()
        await ctx.respond('Databae cleared!')
    
    @discord.slash_command()
    async def gimme(self, ctx):
        user = db.get_user(ctx.author.id)
        user.gain_roll_currency(90)
        await ctx.respond("90 roll currency added")


def setup(bot):
    bot.add_cog(AdminCommands(bot))