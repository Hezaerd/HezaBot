import time
from difflib import get_close_matches

import discord
from discord.ext import commands

from Modules import Utils


class Help(commands.Cog, name="Help"):
    def __init__(self, bot):
        self.bot = bot
        self.loading_time = time.time()

        self.all_commands = None
        self.all_cogs = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Help cog loaded in {round(time.time() - self.loading_time, 2)} seconds')
        self._refresh_commands()
        
    def _refresh_commands(self) -> None:
        """Refresh the list of all commands"""
        self.all_commands = [cmd.name for cmd in self.bot.commands if not cmd.hidden and cmd.name[0].islower()]

    def _refresh_cogs(self) -> None:
        """Refresh the list of all cogs"""
        self.all_cogs = [cog.name for cog in self.bot.cogs.values() if not cog.hidden and cog.name[0].islower()]

    def _embed_default(self) -> discord.Embed:
        """Return an embed for the default help command"""
        embed = discord.Embed(
            title=">help",
            description="Shows help for all commands",
            color=Colors.Embed.Success)

        embed.add_field(
            name="Commands", 
            value="\n".join(self.all_commands), 
            inline=False
        )
        
        return embed
    
    def _embed_cmd_not_found(self, command: str) -> discord.Embed:
        """Return an embed for a command not found"""
        similar_command = get_close_matches(command, self.all_commands, n=1, cutoff=0.5)

        embed = discord.Embed(title="Command not found!", color=Colors.Embed.Error)

        if similar_command:
            embed.colour = Colors.Embed.Similar
            embed.add_field(
                name="Did you mean?", 
                value=similar_command[0], 
                inline=False
            )
        else:
            embed.add_field(
                name="No similar commands found!", 
                value="Try again with a different command.",
                inline=False
            )
        return embed

    def _embed_subcommand_not_found(self, command: str, subcommand: str) -> discord.Embed:
        """Return an embed for a subcommand not found"""
        similar_subcommand = get_close_matches(subcommand, self.bot.get_command(command), n=1, cutoff=0.5)

        embed = discord.Embed(title="Subcommand not found!", color=Colors.Embed.Error)

        if similar_subcommand:
            embed.colour = Colors.Embed.Similar
            embed.add_field(
                name="Did you mean?",
                value=similar_subcommand[0],
                inline=False
            )
        else:
            embed.add_field(
                name="No similar subcommands found!",
                value="Try again with a different subcommand.",
                inline=False
            )
        return embed

    @commands.hybrid_command(
        name="help",
        usage=">help [command/group] [subcommand]"
    )
    async def help(self, ctx: commands.Context, command: str = None, subcommand: str = None) -> None:
        f"""Shows help
        > **Note:** If no command is specified, a list of all commands will be shown.
        > **Note:** If a command is specified, a list of all subcommands will be shown.
        > **Note:** To get help for a subcommand, specify the command and the subcommand.
        (e.g. `>help user avatar`)"""
        if command is None and subcommand is None:
            embed = self._embed_default()
            await ctx.reply(embed=embed)
            return

        if command is not None and subcommand is None:
            if command in self.all_commands:
                cmd = self.bot.get_command(command)
                embed = discord.Embed(
                    title=f"Help for {cmd.name}",
                    description=cmd.help,
                    color=Colors.Embed.Success
                )
                embed.add_field(
                    name="Usage",
                    value=cmd.usage,
                    inline=False
                )
                await ctx.reply(embed=embed)
                return
            else:
                embed = self._embed_cmd_not_found(command)
                await ctx.reply(embed=embed)
                return

        if command is not None and subcommand is not None:
            if command in self.all_commands:
                cmd = self.bot.get_command(command)
                if subcommand in cmd.commands:
                    subcmd = cmd.get_command(subcommand)
                    embed = discord.Embed(
                        title=f"Help for {subcmd.name}",
                        description=subcmd.help,
                        color=Colors.Embed.Success
                    )
                    embed.add_field(
                        name="Usage",
                        value=subcmd.usage,
                        inline=False
                    )
                    await ctx.reply(embed=embed)
                    return
                else:
                    embed = self._embed_subcommand_not_found(command, subcommand)
                    await ctx.reply(embed=embed)
                    return
            else:
                embed = self._embed_cmd_not_found(command)
                await ctx.reply(embed=embed)
                return


async def setup(bot):
    await bot.add_cog(Help(bot))
