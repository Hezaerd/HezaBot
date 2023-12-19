import discord
from discord.ext import commands

import time
import settings
from Modules.DB import DB


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loading_time = time.time()

        self.db = DB().client.heza

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Economy cog loaded in {round(time.time() - self.loading_time, 2)} seconds')

    @commands.hybrid_group(name="economy", aliases=["eco"])
    async def economy(self, ctx):
        """Economy commands"""
        pass

    @economy.command(
        name="balance",
        aliases=["bal", "b", "money", "cash"],
        usage=">economy balance [user]"
    )
    @commands.check(settings.is_registered)
    async def balance(self, ctx, user: discord.Member = None):
        """Check balance"""
        if user is None:
            user = ctx.message.author

        if self.db.users.find_one({"_id": user.id}):
            balance = self.db.users.find_one({"_id": user.id})["balance"]
            await ctx.reply(f"{user}'s balance is {balance}")
        else:
            await ctx.reply(f"{user} is not registered!")

    @economy.command(
        name="balance_top",
        aliases=["baltop", "btop"],
        usage=">economy balance_top"
    )
    async def balance_top(self, ctx):
        """Check balance top"""
        top = self.db.users.find().sort("balance", -1).limit(5)

        embed = discord.Embed(
            title="Balance top",
            description="Top 5 richest users",
            color=discord.Color.gold()
        )

        msg = ""

        for user in top:
            msg += f"<@{user['_id']}> - {user['balance']}\n"

        embed.add_field(name="Users", value=msg, inline=True)

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Economy(bot))