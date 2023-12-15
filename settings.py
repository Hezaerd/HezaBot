import os
from discord import User, Guild


# Core
TOKEN: str = os.getenv("TOKEN")
COMMAND_PREFIX: str = os.getenv("COMMAND_PREFIX")

# Debug
OWNER_ID: str = os.getenv("OWNER_ID")
OWNER: User
DEV_GUILD_ID: str = os.getenv("DEV_GUILD_ID")
DEV_GUILD: Guild

# IMGFLIP
IMGFLIP_USERNAME: str = os.getenv("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD: str = os.getenv("IMGFLIP_PASSWORD")
