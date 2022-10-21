import discord
from discord.ext import commands

class MyView(discord.ui.View):
    #@discord.ui.button(label="Punch", style=discord.ButtonStyle.primary, emoji="🔘")
    @discord.ui.button(label="Punch", style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        button.disabled = True
        #await interaction.response.send_message("You clickied")
        await interaction.response.edit_message(view=self)

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
        embed = discord.Embed()
        embed.title = "Fight"
        embed.thumbnail = ctx.author.display_avatar
        embed.image = "https://media.discordapp.net/attachments/1015443526567346237/1032033260441718916/FfWytuRX0AAYiY_.jpg"
        await ctx.respond(embed=embed)



def setup(bot):
    bot.add_cog(MainMenu(bot))

###   https://guide.pycord.dev/interactions/ui-components/buttons

### https://docs.pycord.dev/en/master/api.html?highlight=respond#discord.ApplicationContext.respond