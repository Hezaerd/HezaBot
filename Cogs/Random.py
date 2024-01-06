import time
import random

from discord.ext import commands
from discord.ext.commands.view import StringView


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.tag = __class__.__name__
        self.startup_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.info(f"Cog.{self.tag}",
                             f"Loaded in {round(time.time() - self.startup_time, 2)}s")

    @commands.hybrid_group(
        name="random",
        usage=">random <subcommand>",
    )
    async def random(self, ctx):
        """Random commands"""
        pass

    @random.command(
        name="rand",
        usage=">random rand <min> <max>",
    )
    async def rand(self, ctx, min: int, max: int):
        """Returns a random number between min and max"""
        if min > max:
            await ctx.reply("min must be less than max")
            return

        await ctx.reply(f"Your random number is: **{random.randint(min, max)}**")
        

async def setup(bot):
    await bot.add_cog(Random(bot))
