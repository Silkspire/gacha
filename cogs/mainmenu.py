import discord
from discord.ext import commands
import asyncio
from random import randint
import db
import classes

class MyView(discord.ui.View):
    #@discord.ui.button(label="Punch", style=discord.ButtonStyle.primary, emoji="🔘")
    @discord.ui.button(label="Punch", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        button.disabled = True
        #await interaction.response.send_message("You clickied")
        await interaction.response.edit_message(view=self)

class Player():
    def __init__(self, health=100, attack=35):
        self.max_hp = health
        self.hp = health
        self.atk = attack
    def damage(self, amount):
        self.hp -= amount
        return amount

class Enemy():
    def __init__(self, health=100, attack=20):
        self.max_hp = health
        self.hp = health
        self.atk = attack
    def damage(self, amount):
        self.hp -= amount
        return amount

class GameState():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = '0'
        self.log_list = ['⠀','⠀','⠀',"Fight has started"]
        self.log = '\n'.join(self.log_list)
    def add_log(self, line: str):
        self.log_list.append(line)
        self.log = '\n'.join(self.log_list)
        self.log_list.pop(0)
    def next_turn(self):
        self.turn = str(int(self.turn) + 1)


def player_turn(game):
    dmg = game.enemy.damage(randint(game.player.atk-int(game.player.atk*0.5), game.player.atk+int(game.player.atk*1.5)))
    game.add_log(f"P{game.turn}: Player attacked Enemy for {dmg} damage")
    return game

def enemy_turn(game):
    dmg = game.player.damage(randint(game.enemy.atk-int(game.enemy.atk*0.5), game.enemy.atk+int(game.enemy.atk*1.5)))
    game.add_log(f"E{game.turn}: Enemy attacked Player for {dmg} damage")
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

    
    @discord.slash_command()
    async def test(self, ctx):
        await ctx.respond("This is a test", ephemeral=True)

    @discord.user_command()
    async def test_user(self, ctx, member: discord.Member):
        await ctx.respond(f'{ctx.author.mention} says hello to {member.name}')
    
    @discord.slash_command()
    async def button_test(self, ctx):
        await ctx.respond("do it", view=MyView())

    @discord.slash_command()
    async def test_fight(self, ctx):
    # OOP tho
    # TODO: turn "status" into OOP class
        user = db.check_user(ctx.author.id)
        db.instantiate_character(user.id, 1)
        player = Player(randint(1,1000), randint(75,150))
        enemy = Enemy(randint(1,1000), randint(75,150))
        game = GameState(player, enemy)
        #log = 'Fight started'
        # char_health = 100
        # enemy_health = 100
        # char_atk = 35
        # enemy_atk = 20
        embed = discord.Embed()
        embed.title = "Fight"
        embed.set_thumbnail(url = ctx.author.display_avatar.url)
        embed.add_field(name = 'Turn', value = game.turn)
        embed.add_field(name = 'Player Health', value = f'{game.player.max_hp}/{game.player.max_hp}')
        embed.add_field(name = 'Enemy Health', value = f'{game.enemy.max_hp}/{game.enemy.max_hp}')
        embed.add_field(name = 'Combat Log', value = game.log)
        embed.set_image(url="https://media.discordapp.net/attachments/1015443526567346237/1032033260441718916/FfWytuRX0AAYiY_.jpg")
        message = await ctx.respond(embed=embed)
        #status = (player, enemy)

        while True:
            await asyncio.sleep(2)
            game.next_turn()
            game = player_turn(game)
            embed.set_field_at(0, name = "Turn", value = game.turn)
            embed.set_field_at(1, name = "Player Health", value = f'{game.player.hp}/{game.player.max_hp}')
            embed.set_field_at(2, name = "Enemy Health", value = f'{game.enemy.hp}/{game.enemy.max_hp}')
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
            embed.set_field_at(1, name = "Player Health", value = f'{game.player.hp}/{game.player.max_hp}')
            embed.set_field_at(2, name = "Enemy Health", value = f'{game.enemy.hp}/{game.enemy.max_hp}')
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