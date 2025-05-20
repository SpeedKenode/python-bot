import discord
from discord.ext import commands
import time

class information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["server"])
    async def serverinfo(self, ctx):
        embed = discord.Embed()
        embed.add_field(name="👑 Owner", value=ctx.guild.owner.mention, inline=True)
        embed.add_field(name="🆔Server ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="📆 Date created", value=f"<t:{int(time.mktime(ctx.guild.created_at.timetuple()))}:R>", inline=True)
        embed.add_field(name="👥 Members", value=f"Users: {len([m for m in ctx.guild.members if not m.bot])} \n Bots: {len([m for m in ctx.guild.members if m.bot])}", inline=True)
        embed.add_field(name="💬 Channels", value=f"#️⃣ {len(ctx.guild.text_channels)} Text \n 🔊 {len(ctx.guild.voice_channels)} Voice", inline=True)
        embed.add_field(name="📜Roles", value=f"{len(ctx.guild.roles) - len([m for m in ctx.guild.members if m.bot]) - 1}", inline=True)
        embed.add_field(name="🌏 Verification Levels", value=f"{str(ctx.guild.verification_level)}", inline=True)
        embed.add_field(name=f"💠 Server boost (LvL {ctx.guild.premium_tier})", value=f"💎Boosters: {len(ctx.guild.premium_subscribers)}", inline=True)
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        embed.set_thumbnail(url=ctx.guild.icon)
        embed.set_image(url=ctx.guild.banner)
 
        await ctx.send("In progress...", embed=embed)
async def setup(bot):
    await bot.add_cog(information(bot))
        