from discord.ext import commands
import time


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.startup_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.logger.trace("Cog.Test",
                              f"Loaded Cog {self.__class__.__name__} in {round(time.time() - self.startup_time, 2)}s")


async def setup(bot):
    await bot.add_cog(Test(bot))
