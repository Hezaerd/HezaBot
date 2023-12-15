import time
from datetime import datetime
from sys import version_info as sysv

import discord
from discord.ext import commands

import settings


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

    @commands.hybrid_group(
        name="debug",
        usage=">debug [command]"
    )
    async def debug(self, ctx: commands.Context) -> None:
        """Debug utils for the bot (or client)"""
        pass

    @debug.command(
        name="ping",
        usage=">debug ping"
    )
    async def ping(self, ctx: commands.Context) -> None:
        """:ping_pong: Send a ping request"""
        embed = discord.Embed(title=":ping_pong: Pong!",
                              description=f'Latency: `{round(self.bot.latency * 1000)}ms`',
                              color=0x0099ff,
                              timestamp=datetime.utcnow())
        embed.set_footer(text=f'{ctx.message.author.name}\n',
                         icon_url=ctx.message.author.avatar)
        await ctx.reply(embed=embed)

    @debug.command(
        name="info",
        usage=">debug info"
    )
    async def info(self, ctx: commands.Context) -> None:
        embed = discord.Embed(title="HezaBot",
                              description="A multi function bot!",
                              colour=0x00b0f4,
                              timestamp=datetime.now())

        embed.add_field(name="Owner :crown:",
                        value=f'[{settings.OWNER}](https://github.com/Hezaerd)',
                        inline=False)
        embed.add_field(name="Discord.py :",
                        value=f'{discord.__version__}',
                        inline=True)
        embed.add_field(name="Python :",
                        value=f'{sysv.major}.{sysv.minor}.{sysv.micro}',
                        inline=True)
        embed.add_field(name="Source code :",
                        value="[Github](https://github.com/Hezaerd/HezaBot)",
                        inline=True)
        embed.add_field(name="Tips:",
                        value="Use `>help` to know where to start!",
                        inline=True)

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/1181640113239900303/b71bc57ef9b51c2ab9e060d8a39eecff.png?size=1024")

        embed.set_footer(text="Made with ❤️ by Hezaerd",
                         icon_url="https://cdn.discordapp.com/avatars/225942632050720768"
                                  "/a_360dbeff591c32cb664950aab0a5a6c8.gif?size=1024")

        await ctx.reply(embed=embed)

    @commands.command(name="invite", aliases=["link"], usage=">invite")
    async def invite(self, ctx: commands.Context) -> None:
        """Get the invite link for the bot"""
        await ctx.reply(
            f'**Invite link:** <https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8'
            f'&scope=bot>')

    @commands.group(
        name="sync",
        usage=">sync [dev/global]",
        hidden=True
    )
    @commands.is_owner()
    async def sync(self, ctx: commands.Context) -> None:
        """Sync commands"""
        pass

    @sync.command(
        name="dev",
        usage=">sync dev",
        hidden=True
    )
    @commands.is_owner()
    async def sync_dev(self, ctx: commands.Context) -> None:
        """Sync commands to dev guild"""
        synced = await self.bot.tree.sync(guild=settings.DEV_GUILD_ID)
        print(f'  [Debug]: Synced {len(synced)} commands to {settings.DEV_GUILD_ID}')
        await ctx.send(f'Synced {len(synced)} commands to {settings.DEV_GUILD_ID}')

    @sync.command(
        name="global",
        usage=">sync global",
        hidden=True
    )
    @commands.is_owner()
    async def sync_global(self, ctx: commands.Context) -> None:
        """Sync commands globally"""
        synced = await self.bot.tree.sync()
        print(f'  [Debug]: Synced {len(synced)} commands globally')
        await ctx.send(f'Synced {len(synced)} commands globally')


async def setup(bot):
    await bot.add_cog(Debug(bot))
