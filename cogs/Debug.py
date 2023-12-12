from discord.ext import commands
import discord
from sys import version_info as sysv
import settings

class Debug(commands.Cog, name="Debug"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.dev_guild = await self.bot.fetch_guild(settings.DEV_GUILD_ID)

        print(f'Debug cog loaded')

        print(f'  [Debug]: Python version: {sysv.major}.{sysv.minor}.{sysv.micro}')
        print(f'  [Debug]: Discord.py version: {discord.__version__}')
        print(f'  [Debug]: Dev guild: {self.dev_guild}')

    @commands.hybrid_command(name="ping", usage=">ping")
    async def ping(self, ctx: commands.Context) -> None:
        ''':ping_pong: Send a ping request'''
        embed = discord.Embed(title=":ping_pong: Pong!", description=f'Latency: `{round(self.bot.latency * 1000)}ms`', color=0x0099ff)    
        embed.set_footer(text=f'{ctx.message.author.name}\n' + f'Today at {ctx.message.created_at.strftime("%I:%M")}', icon_url=ctx.message.author.avatar)
        # embed.set_footer(text=f'{ctx.author}', icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(name="sync", usage=">sync", hidden=True)
    @commands.is_owner()
    async def sync(self, ctx):
        '''Sync commands to dev guild'''
        synced = await self.bot.tree.sync(guild=settings.DEV_GUILD_ID)
        print(f'  [Debug]: Synced {len(synced)} commands to {settings.DEV_GUILD_ID}')
        await ctx.send(f'Synced {len(synced)} commands to {settings.DEV_GUILD_ID}')

    @commands.command(name="syncglobal", usage=">syncglobal", hidden=True)
    @commands.is_owner()
    async def syncglobal(self, ctx):
        '''Sync commands globally'''
        synced = await self.bot.tree.sync()
        print(f'  [Debug]: Synced {len(synced)} commands globally')
        await ctx.send(f'Synced {len(synced)} commands globally')        
        
async def setup(bot):
    await bot.add_cog(Debug(bot))