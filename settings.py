import os
from Modules.DB import DB
from discord.ext import commands
import discord


# Bot
TOKEN: str = os.getenv("TOKEN")
COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX")

# OWNER
OWNER_ID: str = os.getenv("OWNER_ID")
DEV_GUILD_ID: str = os.getenv("DEV_GUILD_ID")

# MONGODB
MONGODB_URL: str = os.getenv("MONGODB_URL")

# IMGFLIP
IMGFLIP_USERNAME: str = os.getenv("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD: str = os.getenv("IMGFLIP_PASSWORD")

# ECONOMY
CURRENCY = ":moneybag:"


async def is_registered(ctx: commands.Context, user: discord.Member = None) -> bool:
    """Check if user is registered"""
    if user is None:
        user = ctx.message.author

    if DB().client.heza.users.find_one({"_id": user.id}):
        return True
    else:
        await ctx.reply(f"You can't perform this action, you are not registered!")
        return False
