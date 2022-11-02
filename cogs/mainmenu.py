import discord
from discord.ext import commands
import asyncio
from random import randint
import db
from discord import option
from typing import Optional

from classes.BaseCharacter import *
from classes.Enemy import *
from classes.GameState import *
from classes.InstantiatedCharacter import *
from classes.Monster import *
from classes.Player import *
from classes.User import *

class MyView(discord.ui.View):
    #@discord.ui.button(label="Punch", style=discord.ButtonStyle.primary, emoji="🔘")
    @discord.ui.button(label="Punch", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        button.disabled = True
        #await interaction.response.send_message("You clickied")
        await interaction.response.edit_message(view=self)


def player_turn(game):
    #dmg = enemy damage +- 25%
    dmg = game.enemy.damage(randint(game.player.attack-int(game.player.attack*0.75), game.player.attack+int(game.player.attack*1.25)))
    game.add_log(f"P{game.round}: Player attacked Enemy for {dmg} damage")
    return game

def enemy_turn(game):
    #dmg = player damage +- 25%
    dmg = game.player.damage(randint(game.enemy.attack-int(game.enemy.attack*0.75), game.enemy.attack+int(game.enemy.attack*1.25)))
    game.add_log(f"E{game.round}: Enemy attacked Player for {dmg} damage")
    return game

def win(game):
    if game.enemy.hp <= 0:
        game.add_log("**Victory achieved**")
        return True
    else:
        return False

def loss(game):
    if game.player.hp <= 0:
        game.add_log("**You Lost**")
        return True
    else:
        return False

class MainMenu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    # @discord.slash_command()
    # async def test(self, ctx):
    #     await ctx.respond("This is a test", ephemeral=True)

    # @discord.user_command()
    # async def test_user(self, ctx, member: discord.Member):
    #     await ctx.respond(f'{ctx.author.mention} says hello to {member.name}')
    
    # @discord.slash_command()
    # async def button_test(self, ctx):
    #     await ctx.respond("do it", view=MyView())

    # @discord.slash_command()
    # async def buy_character(self, ctx):
    #     pass

    @discord.slash_command()
    async def check_roll_currency(self, ctx):
        user = await self.check_user(ctx)
        if not user:
            return
        currency = user.check_roll_currency()
        await ctx.respond(f"You have {currency} roll currency.")

    @discord.slash_command(name='buy_character_pack')
    @option(
        'number',
        int,
        description='How many characters to buy',
        required=False,
        choices=[1, 10]
    )
    async def buy_pack(self, ctx, *, number: Optional[int] = 1):
        user = await self.check_user(ctx)
        if not user:
            return
        if user.roll_currency < number * 1:
            await ctx.respond(f"{number} roll currency needed, you only have {user.roll_currency}")
            return
        character_ids = db.gacha_character(user.id, number)
        user.spend_roll_currency((number*1))
        output = 'Received:\n'
        for id in character_ids:
            char=db.get_base_character(id)
            output+=char.name+'\n'
        await ctx.respond(output)


    async def select_starter(self, user, interaction):
        # TODO: change from command to auto-thing

        #user = db.get_user(ctx.author.id)
        text = ""
        starter_characters = ['1', '2', '3']
        for char in starter_characters:
            text+=char+'\n'

        class MyView(discord.ui.View):
            @discord.ui.button(label=starter_characters[0], style=discord.ButtonStyle.primary)
            async def button1_callback(self, button, interaction):
                await interaction.response.send_message(f"You selected {starter_characters[0]}!")
            @discord.ui.button(label=starter_characters[1], style=discord.ButtonStyle.primary)
            async def button2_callback(self, button, interaction):
                await interaction.response.send_message(f"You selected {starter_characters[1]}!")
            @discord.ui.button(label=starter_characters[2], style=discord.ButtonStyle.primary, emoji="😎")
            async def button3_callback(self, button, interaction):
                await interaction.response.send_message(f"You selected {starter_characters[2]}!")

        await interaction.response.edit_message(content=text, view=MyView())


    async def user_startup(self, ctx):
        select_starter = self.select_starter
        # TODO: privacy policy link
        # short description of game?
        class MyView(discord.ui.View):
            @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
            async def button_callback_yes(self, button, interaction):
                user = db.add_user(ctx.author.id)
                await select_starter(user, interaction)
                #await interaction.response.edit_message(view=newView())#self)
                #await interaction.response.send_message(f"You selected {starter_characters[0]}!")
            @discord.ui.button(label='No', style=discord.ButtonStyle.red)
            async def button_callback_no(self, button, interaction):
                await interaction.delete_original_response(delay=2)
                #await interaction.response.edit_message(view=newView())
                #await interaction.response.send_message(f"You selected {starter_characters[0]}!")
        await ctx.respond("Do you want to play a game?", view=MyView())



    async def check_user(self, ctx):
        user = db.get_user(ctx.author.id)
        if user:
            return user
        else:
            await self.user_startup(ctx)
            return False



    @discord.slash_command()
    async def select_character(self, ctx):
        options = []
        
        user = await self.check_user(ctx)
        if not user:
            return

        characters = db.get_owned_characters(user.id)
        for char in characters:
            options.append(discord.SelectOption(
                    label=f"{char[0]}: {char[1]}",
                    value=str(char[0]),
                    description='this is a desc'
                ))

        class MyView(discord.ui.View):
            @discord.ui.select(
                placeholder = "Select character",
                options = options,
            )
            async def select_callback(self, select, interaction):
                user.switch_selected_character(select.values[0])
                await interaction.response.send_message(f"Selected {select.values[0]}")
        view=MyView()
        # TODO?: remove the selector after user interaction
        # it keeps working tho
        await ctx.respond(view=view, ephemeral=True)

    @discord.slash_command()
    async def test_fight(self, ctx):
        difficulty = 'easy'
        user = await self.check_user(ctx)
        if not user:
            return
        player = Player(db.get_selected_character(user.id))

        enemy = Enemy(db.get_monster(difficulty))
        game = GameState(player, enemy)
        #log = 'Fight started'
        # char_health = 100
        # enemy_health = 100
        # char_attack = 35
        # enemy_attack = 20
        embed = discord.Embed()
        embed.title = f"Fight ({player.id})"
        embed.set_thumbnail(url = player.image)
        embed.add_field(name = 'Round', value = game.round)
        embed.add_field(name = 'Player Health', value = f'{game.player.max_health}/{game.player.max_health}')
        embed.add_field(name = 'Enemy Health', value = f'{game.enemy.max_health}/{game.enemy.max_health}')
        embed.add_field(name = 'Combat Log', value = game.log)
        embed.set_image(url = enemy.image)
        message = await ctx.respond(embed=embed)
        #status = (player, enemy)

        while True:
            await asyncio.sleep(2)
            game.next_round()
            game = player_turn(game)
            embed.set_field_at(0, name = "Round", value = game.round)
            embed.set_field_at(1, name = "Player Health", value = f'{game.player.hp}/{game.player.max_health}')
            embed.set_field_at(2, name = "Enemy Health", value = f'{game.enemy.hp}/{game.enemy.max_health}')
            embed.set_field_at(3, name = "Combat Log", value=game.log)
            if win(game):
                #embed.add_field(name='Victory', value='Yay')
                embed.set_field_at(3, name = "Combat Log", value=game.log)
                await message.edit_original_response(embed=embed)
                return
            else:
                await message.edit_original_response(embed=embed)
            await asyncio.sleep(2)
            game = enemy_turn(game)
            embed.set_field_at(1, name = "Player Health", value = f'{game.player.hp}/{game.player.max_health}')
            embed.set_field_at(2, name = "Enemy Health", value = f'{game.enemy.hp}/{game.enemy.max_health}')
            embed.set_field_at(3, name = "Combat Log", value=game.log)
            if loss(game):
                #embed.add_field(name='Loss', value='oh no')
                embed.set_field_at(3, name = "Combat Log", value=game.log)
                await message.edit_original_response(embed=embed)
                return
            else:
                await message.edit_original_response(embed=embed)

    @discord.slash_command()
    async def menu(self, ctx):
        await ctx.respond("Menu Placeholder")

def setup(bot):
    bot.add_cog(MainMenu(bot))

###   https://guide.pycord.dev/interactions/ui-components/buttons

### https://docs.pycord.dev/en/master/api.html?highlight=respond#discord.ApplicationContext.respond