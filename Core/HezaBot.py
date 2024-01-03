import discord
from discord.ext import commands
import os

from Core.Logger import Logger


class HezaBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=">", intents=discord.Intents.all(), help_command=None)

        self.logger = Logger()

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        """Starts the bot"""
        await super().start(token, reconnect=reconnect)

    async def close(self) -> None:
        """Closes the bot"""
        await super().close()

    async def on_ready(self) -> None:
        """Event that fires when the bot is ready"""
        self.logger.success(f"Logged in as {self.user}")

    async def load_all_extensions(self) -> None:
        """Loads all extensions"""
        self.logger.info("Loading all extensions")

        for filename in os.listdir("./Cogs"):
            if filename.endswith(".py"):
                self.logger.info(f"Found extension {filename}")
                await self.load_extension(f"Cogs.{filename[:-3]}")

        self.logger.success("Loaded all extensions")

    async def unload_all_extensions(self) -> None:
        """Unloads all extensions"""
        self.logger.info("Unloading all extensions")

        for filename in os.listdir("Cogs"):
            if filename.endswith(".py"):
                await self.unload_extension(f"Cogs.{filename[:-3]}")

        self.logger.info("Unloaded all extensions")

    async def reload_all_extensions(self) -> None:
        """Reloads all extensions"""
        self.logger.info("Reloading all extensions")
        await self.unload_all_extensions()
        await self.load_all_extensions()
        self.logger.info("Reloaded all extensions")
