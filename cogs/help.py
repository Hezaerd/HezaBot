from discord.ext import commands
import discord
from difflib import get_close_matches
import time

class Help(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot
        self.loading_time = time.time()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Help cog loaded in {round(time.time() - self.loading_time, 2)} seconds')

        self.all_commands = [cmd.name for cmd in self.bot.commands if not cmd.hidden and cmd.name[0].islower()]

    def _similar(self, command):
        '''Look for a similar command'''
        return get_close_matches(command, self.all_commands, n=1, cutoff=0.5)

    @commands.hybrid_command(name="help", aliases=["h"], usage=">help [command]")
    async def help(self, ctx, command: str = None):
        '''Shows help'''
        if command is None:
            embed = discord.Embed(title="Help", description=f"Use `{self.bot.command_prefix}help [command]` for more info on a command.", color=0x00ff00)
            for cog in self.bot.cogs:
                cog_commands = self.bot.get_cog(cog).get_commands()
                if len(cog_commands) != 0:
                    filtered_commands = [cmd for cmd in cog_commands if not cmd.hidden and cmd.name[0].islower()]  # Exclude hidden commands and gears
                    if len(filtered_commands) != 0:
                        embed.add_field(name=cog, value=f"`{', '.join([command.name for command in filtered_commands])}`", inline=False)
            await ctx.reply(embed=embed)
        else:
            user_command = command
            command = self.bot.get_command(command)
            if command is None or command.hidden or command.name[0].isupper():  # Exclude hidden commands and gears
                similar_command = self._similar(user_command)
                embed = discord.Embed(title="Command not found!", color=0xff0000)
                if similar_command:
                    embed.add_field(name="Did you mean?", value=similar_command[0], inline=False)
                else:
                    embed.add_field(name="No similar commands found!", value="Try again with a different command.", inline=False)
                await ctx.reply(embed=embed)
                return
            embed = discord.Embed(title=f"Help: {command.name}", description=command.help, color=0x00ff00)
            if len(command.aliases) != 0:
                embed.add_field(name="Aliases", value=", ".join(command.aliases), inline=False)
            embed.add_field(name="Usage", value=command.usage, inline=False)  # Add the usage field
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))