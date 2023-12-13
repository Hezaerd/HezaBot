from discord.ext import commands
import discord
from sys import version_info as sysv
import settings
import time


class Debug(commands.Cog):
    def __init__(self, bot):
        self.dev_guild = None
        self.bot = bot
        self.loading_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        self.dev_guild = await self.bot.fetch_guild(settings.DEV_GUILD_ID)

        print(f'Debug cog loaded in {round(time.time() - self.loading_time, 2)} seconds')

        print(f'  [Debug]: Python version: {sysv.major}.{sysv.minor}.{sysv.micro}')
        print(f'  [Debug]: Discord.py version: {discord.__version__}')
        print(f'  [Debug]: Dev guild: {self.dev_guild}')

    @commands.hybrid_command(name="ping", usage=">ping")
    async def ping(self, ctx: commands.Context) -> None:
        """:ping_pong: Send a ping request"""
        embed = discord.Embed(title=":ping_pong: Pong!", description=f'Latency: `{round(self.bot.latency * 1000)}ms`',
                              color=0x0099ff)
        embed.set_footer(text=f'{ctx.message.author.name}\n' + f'Today at {ctx.message.created_at.strftime("%I:%M")}',
                         icon_url=ctx.message.author.avatar)
        await ctx.reply(embed=embed)

    @commands.command(name="invite", aliases=["link"], usage=">invite")
    async def invite(self, ctx: commands.Context) -> None:
        """Get the invite link for the bot"""
        await ctx.reply(
            f'**Invite link:** <https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8'
            f'&scope=bot>')

    @commands.group(name="sync", usage=">sync [dev/global]", hidden=True)
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        """Sync commands"""
        pass

    @sync.command(name="dev", usage=">sync dev", hidden=True)
    @commands.is_owner()
    async def sync_dev(self, ctx: commands.Context) -> None:
        """Sync commands to dev guild"""
        synced = await self.bot.tree.sync(guild=settings.DEV_GUILD_ID)
        print(f'  [Debug]: Synced {len(synced)} commands to {settings.DEV_GUILD_ID}')
        await ctx.send(f'Synced {len(synced)} commands to {settings.DEV_GUILD_ID}')

    @sync.command(name="global", usage=">sync global", hidden=True)
    @commands.is_owner()
    async def sync_global(self, ctx: commands.Context) -> None:
        """Sync commands globally"""
        synced = await self.bot.tree.sync()
        print(f'  [Debug]: Synced {len(synced)} commands globally')
        await ctx.send(f'Synced {len(synced)} commands globally')


async def setup(bot):
    await bot.add_cog(Debug(bot))
