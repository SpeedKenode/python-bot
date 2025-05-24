import discord
from discord.ext import commands
import asyncio
import random

class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def giveaway(self, ctx, id: int): 
        msg = await ctx.send("Hello! Here's a cool embed.")
        print(msg.id)
        cursor = await self.bot.db.cursor()
        await cursor.execute("""SELECT user_id FROM user WHERE user_id = ?""", (id,))
        re = await cursor.execute("""INSERT INTO USER(USER_ID) VALUES(?)""", (id,))
        await self.bot.db.commit()
    
    @commands.command()
    async def gstart(self, ctx):
        def convert(time):
            pos = ["s", "m", "h", "d"]
            time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400}

            unit = time[-1]

            if unit not in pos:
                return -1
            try:
                val = int(time[:-1])
            except:
                return -2
            
            return val * time_dict[unit]
        
        await ctx.send("Start GA")
        await asyncio.sleep(2)
        questions = ["Channels ?", "Duration ?", "Prize ?", "Winners ?"]
        answers = []
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        for i in questions:
            await ctx.send(i)

            try:
                msg = await self.bot.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("TIME'S UP")
                return
            else:
                answers.append(msg.content)
            
        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send("Invallid")
            return
        
        channel = self.bot.get_channel(c_id)

        time = convert(answers[1])
        if time == -1:
            await ctx.send("Invalid")
            return
        elif  time == -2:
            await ctx.send("Invalid")
            return
        
        prizes = answers[2]
        winnerscount = int(answers[3])

        await ctx.send("GA is starting")

        embed = discord.Embed(title="Giveaway", description=f"{prizes}")
        embed.add_field(name="Host", value=ctx.author.mention)
        embed.add_field(name="Winners", value=f"{winnerscount}")
        embed.set_footer(text=f"Ends {answers[1]} from now")

        my_msg = await channel.send(embed = embed)

        await my_msg.add_reaction("🎉")
        await asyncio.sleep(time)

        new_msg = await channel.fetch_message(my_msg.id)
        users = [user async for user in new_msg.reactions[0].users()]
        users.pop(users.index(self.bot.user))

        if len(users) == 0:
            await ctx.send("No winners")
        else:
            roll = 0
            if winnerscount < len(users):
                roll = winnerscount
            else:
                roll = len(users)
            winners = random.sample(users, roll)
            
            winners_list = " ".join([f"<@{user.id}>" for user in winners])
            
        await channel.send(f"Done. Winners is {winners_list}")


async def setup(bot):
    await bot.add_cog(giveaway(bot))