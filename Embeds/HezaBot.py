from datetime import datetime
from sys import version_info as sysv

import discord

import settings


def embed() -> discord.Embed:
    """Get info about the bot"""
    print('[Embed: HezaBot]: Called!')

    _embed = discord.Embed(title="HezaBot",
                           description="A multi function bot!",
                           colour=0x00b0f4,
                           timestamp=datetime.now()
                           )
    print('[Embed: HezaBot]: Created embed')
    _embed.add_field(name="Owner :crown:",
                     value=f'[Hezaerd](https://github.com/Hezaerd)',
                     inline=False)
    print('[Embed: HezaBot]: Added owner field')
    _embed.add_field(name="Discord.py :",
                     value=f'{discord.__version__}',
                     inline=True)
    print('[Embed: HezaBot]: Added discord.py field')
    _embed.add_field(name="Python :",
                     value=f'{sysv.major}.{sysv.minor}.{sysv.micro}',
                     inline=True)
    print('[Embed: HezaBot]: Added python field')
    _embed.add_field(name="Source code :",
                     value="[Github](https://github.com/Hezaerd/HezaBot)",
                     inline=True)
    print('[Embed: HezaBot]: Added source code field')
    _embed.add_field(name="Tips:",
                     value="Use `>help` to know where to start!",
                     inline=True)
    print('[Embed: HezaBot]: Added tips field')

    _embed.set_thumbnail(
        url="https://cdn.discordapp.com/avatars/1181640113239900303/b71bc57ef9b51c2ab9e060d8a39eecff.png?size=1024"
    )
    print('[Embed: HezaBot]: Added thumbnail')

    _embed.set_footer(text="Made with ❤️ by Hezaerd",
                      icon_url="https://cdn.discordapp.com/avatars/225942632050720768"
                               "/a_360dbeff591c32cb664950aab0a5a6c8.gif?size=1024"
                      )
    print('[Embed: HezaBot]: Added footer')

    return _embed
