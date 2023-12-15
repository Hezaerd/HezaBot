from itertools import cycle
from os import listdir

import discord
from discord.ext import commands, tasks

import settings

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX, intents=intents, help_command=None)

cogs_cache = []


@bot.event
async def on_ready():
    print('------')
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator} (ID: {bot.user.id})')
    print(f'Serving {len(bot.guilds)} guilds & {len(bot.users)} users')
    print('------')

    await bot.tree.sync(guild=discord.Object(id=settings.DEV_GUILD_ID))
    print(f'Synced {len(bot.tree)} commands to {settings.DEV_GUILD_ID}')


status = cycle([
    'Pythoning',
    'Doing stuff...',
    'Being a bot'
])


@tasks.loop(minutes=1)
async def change_presence():
    new_status = next(status)
    await bot.change_presence(activity=discord.Game(new_status))
    print('Status changed to ' + new_status)


@change_presence.before_loop
async def before_change_presence():
    """Only runs once"""
    await bot.wait_until_ready()


@bot.check
async def block_dms(ctx):
    """Block commands in DMs"""
    return ctx.guild is not None


async def load_cogs():
    import time
    start_time = time.time()

    print('------')
    print('Loading cogs... (multi-threaded)')

    for filename in listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'Cog found: {filename[:-3]} ({round(time.time() - start_time, 2)} seconds)')
            await bot.load_extension(f'cogs.{filename[:-3]}')
            cogs_cache.append(filename[:-3])

    print(f'Found {len(bot.cogs)} cogs in {round(time.time() - start_time, 2)} seconds')
    print('------')


async def unload_cogs():
    import time
    start_time = time.time()

    cogs = 0

    for cog in cogs_cache:
        print(f'Cog unloaded: {cog} in {round(time.time() - start_time, 2)} seconds (cached)')
        await bot.unload_extension(f'cogs.{cog}')
        cogs += 1

    print(f'Unloaded {cogs} cogs in {round(time.time() - start_time, 2)} seconds (cached)')


async def main():
    change_presence.start()
    await load_cogs()
    await bot.start(settings.TOKEN)

    settings.DEV_GUILD = await bot.fetch_guild(settings.DEV_GUILD_ID)
    settings.OWNER = await bot.fetch_user(settings.OWNER_ID)


if __name__ == '__main__':
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('------')
        print('KeyboardInterrupt')
        print('------')
        print('Unloading cogs...')
        asyncio.run(unload_cogs())
        print('------')
        print('Closing bot...')
        asyncio.run(bot.close())
