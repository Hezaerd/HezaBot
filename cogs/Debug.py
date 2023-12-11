from discord.ext import commands
import discord
from sys import version_info as sysv
from os import listdir

class Debug(commands.Cog, name="Debug"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Debug cog loaded')

        print(f'  [Debug]: Python version: {sysv.major}.{sysv.minor}.{sysv.micro}')
        print(f'  [Debug]: Discord.py version: {discord.__version__}')

    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(Debug(bot))