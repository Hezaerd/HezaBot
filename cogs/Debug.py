from discord.ext import commands
import discord
from sys import version_info as sysv
import env

class Debug(commands.Cog, name="Debug"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Debug cog loaded')

        print(f'  [Debug]: Python version: {sysv.major}.{sysv.minor}.{sysv.micro}')
        print(f'  [Debug]: Discord.py version: {discord.__version__}')

    @commands.hybrid_command(name="ping")
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.reply(f':ping_pong: **Pong!** ``{round(self.bot.latency * 1000)}ms``')

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx):
        synced = await self.bot.tree.sync(guild=env.DEV_GUILD_ID)
        print(f'  [Debug]: Synced {len(synced)} commands to {env.DEV_GUILD_ID}')
        await ctx.send(f'Synced {len(synced)} commands to {env.DEV_GUILD_ID}')

    @commands.command(name="syncglobal")
    @commands.is_owner()
    async def syncglobal(self, ctx):
        synced = await self.bot.tree.sync()
        print(f'  [Debug]: Synced {len(synced)} commands globally')
        await ctx.send(f'Synced {len(synced)} commands globally')        
        
async def setup(bot):
    await bot.add_cog(Debug(bot))