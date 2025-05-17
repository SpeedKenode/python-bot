import discord
from discord.ext import commands

class embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(
        title="My Amazing Embed",
        description="Embeds are super easy, barely an inconvenience.",
        color=discord.Colour.blurple(),
    )
        embed.add_field(name="A Normal Field", value="A really nice field with some information. **The description as well as the fields support markdown!**")
        embed.add_field(name="Inline Field 1", value="Inline Field 1", inline=True)
        embed.add_field(name="Inline Field 2", value="Inline Field 2", inline=True)
        embed.add_field(name="Inline Field 3", value="Inline Field 3", inline=True)
        embed.set_footer(text="Footer! No markdown here.")
        embed.set_author(name="Pycord Team", icon_url="https://guide.pycord.dev/img/logo.png")
        embed.set_thumbnail(url="https://guide.pycord.dev/img/logo.png")
        embed.set_image(url="https://guide.pycord.dev/img/banner-v3.png")
 
        await ctx.reply("Hello! Here's a cool embed.", embed=embed)

async def setup(bot):
    await bot.add_cog(embed(bot))