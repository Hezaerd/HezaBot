import time
from random import randint

import discord
from discord.ext import commands

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
            await ctx.reply(f"You currently have {balance} {settings.CURRENCY}")
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
            msg += f"<@{user['_id']}>: {user['balance']} {settings.CURRENCY}\n"

        embed.add_field(name="Users", value=msg, inline=True)

        await ctx.reply(embed=embed)

    @economy.command(
        name="hourly",
        aliases=["h"],
        usage=">economy hourly"
    )
    async def hourly(self, ctx):
        """Get hourly reward"""
        if self.db.users.find_one({"_id": ctx.author.id}):
            user = self.db.users.find_one({"_id": ctx.author.id})

            # check if the entry [last_hourly] exists
            if "last_hourly" not in user:
                self.db.users.update_one({"_id": ctx.author.id}, {"$set": {"last_hourly": 0}})
                user = self.db.users.find_one({"_id": ctx.author.id})

            if user["last_hourly"] + 3600 <= time.time():
                gain = randint(65, 80)

                self.db.users.update_one({"_id": ctx.author.id}, {"$set": {"last_hourly": time.time()}})
                self.db.users.update_one({"_id": ctx.author.id}, {"$inc": {"balance": gain}})
                await ctx.reply(f"You got {gain} {settings.CURRENCY}!")
            else:
                await ctx.reply(f"Already claimed hourly reward!\n"
                                f"Next reward: <t:{int(user['last_hourly'] + 3600)}:R>")
        else:
            await ctx.reply(f"{ctx.author} is not registered!")

    @economy.command(
        name="daily",
        aliases=["d"],
        usage=">economy daily"
    )
    async def daily(self, ctx):
        """Get daily reward"""
        if self.db.users.find_one({"_id": ctx.author.id}):
            user = self.db.users.find_one({"_id": ctx.author.id})

            # check if the entry [last_daily] exists
            if "last_daily" not in user:
                self.db.users.update_one({"_id": ctx.author.id}, {"$set": {"last_daily": 0}})
                user = self.db.users.find_one({"_id": ctx.author.id})

            if user["last_daily"] + 86400 <= time.time():
                gain = randint(500, 600)

                self.db.users.update_one({"_id": ctx.author.id}, {"$set": {"last_daily": time.time()}})
                self.db.users.update_one({"_id": ctx.author.id}, {"$inc": {"balance": gain}})
                await ctx.reply(f"You got {gain} {settings.CURRENCY}!")
            else:
                await ctx.reply(f"Already claimed daily reward!\n"
                                f"Next reward: <t:{int(user['last_daily'] + 86400)}:R>")
        else:
            await ctx.reply(f"{ctx.author} is not registered!")


async def setup(bot):
    await bot.add_cog(Economy(bot))
