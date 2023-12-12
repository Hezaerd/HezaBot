from discord.ext import commands, tasks
from itertools import cycle
from os import listdir
import settings
import discord

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix=settings.COMMAND_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator} (ID: {bot.user.id})')
    print('------')

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
    '''Only runs once'''
    await bot.wait_until_ready()

@bot.check
async def block_dms(ctx):
    '''Block commands in DMs'''
    return ctx.guild is not None

async def load_cogs():
    for filename in listdir('./cogs'):
        if filename.endswith('.py'):
            print(f'Cog found: {filename[:-3]}')
            await bot.load_extension(f'cogs.{filename[:-3]}')
        
async def main():
    change_presence.start()
    await load_cogs()
    await bot.start(settings.TOKEN)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())