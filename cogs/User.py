import time

import discord
from discord.ext import commands
from numerize import numerize

from Modules.DB import DB
from Embeds import HezaBot
import settings


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loading_time = time.time()

        self.db = DB().client.heza

        super().__init__()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f'User cog loaded in {round(time.time() - self.loading_time, 2)} seconds')

    @commands.hybrid_group(
        name="user",
        aliases=["u"],
        usage=">user [subcommand]",
        invoke_without_command=True
    )
    async def user(self, ctx: commands.Context) -> None:
        """User commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @user.command(
        name="register",
        aliases=["reg", "r"],
        usage=">user register"
    )
    async def register(self, ctx: commands.Context) -> None:
        """Register user in database"""
        if self.db.users.find_one({"_id": ctx.author.id}):
            await ctx.reply("You are already registered!")
        else:
            self.db.users.insert_one({"_id": ctx.author.id, "balance": 100})
            await ctx.reply("You have been registered!")

    @user.command(
        name="force_register",
        aliases=["fregister", "fr"],
        usage=">user force_register [user]"
    )
    @commands.is_owner()
    async def force_register(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Force register user in database"""
        if user is None:
            user = ctx.message.author

        if self.db.users.find_one({"_id": user.id}):
            await ctx.reply(f"{user} is already registered!")
        else:
            self.db.users.insert_one({"_id": user.id, "balance": 100})
            await ctx.reply(f"{user} has been registered!")

    @user.command(
        name="force_unregister",
        aliases=["funregister", "fur"],
        usage=">user force_unregister [user]"
    )
    @commands.is_owner()
    async def force_unregister(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Force unregister user from database"""
        if user is None:
            user = ctx.message.author

        if self.db.users.find_one({"_id": user.id}):
            self.db.users.delete_one({"_id": user.id})
            await ctx.reply(f"{user} has been unregistered!")
        else:
            await ctx.reply(f"{user} is not registered!")

    @user.command(
        name="unregister",
        aliases=["unreg", "ur"],
        usage=">user unregister"
    )
    @commands.check(settings.is_registered)
    async def unregister(self, ctx: commands.Context) -> None:
        """Unregister user from database"""
        if self.db.users.find_one({"_id": ctx.author.id}):
            self.db.users.delete_one({"_id": ctx.author.id})
            await ctx.reply("You have been unregistered!")
        else:
            await ctx.reply("You are not registered!")

    @user.command(
        name="is_registered",
        aliases=["is_reg", "ir"],
        usage=">user is_registered [user]"
    )
    @commands.is_owner()
    async def is_registered(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Check if user is registered"""
        if user is None:
            user = ctx.message.author

        if self.db.users.find_one({"_id": user.id}):
            await ctx.reply(f"{user} is registered!")
        else:
            await ctx.reply(f"{user} is not registered!")

    @user.command(
        name="avatar",
        aliases=["pp", "image"],
        usage=">user avatar [user]"
    )
    async def avatar(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Get user avatar"""
        if user is None:
            user = ctx.message.author

        embed = discord.Embed(title=f"{user}'s avatar", color=0xdfa3ff)
        embed.set_image(url=user.avatar)
        await ctx.reply(embed=embed)

    @user.command(
        name="banner",
        aliases=["bn"],
        usage=">user banner [user]"
    )
    async def banner(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Get user banner"""
        if user is None:
            user = ctx.message.author

        user = await self.bot.fetch_user(user.id)

        if user.banner is None:
            await ctx.reply(f"**{user} doesn't have a banner!**")
            return

        embed = discord.Embed(title=f"{user}'s banner", color=0xdfa3ff)
        embed.set_image(url=user.banner)
        await ctx.reply(embed=embed)

    @user.command(
        name="id",
        aliases=["uid"],
        usage=">user id [user]"
    )
    async def id(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Get user ID"""
        if user is None:
            user = ctx.message.author

        embed = discord.Embed(title=f"{user}'s ID", description=user.id, color=0xdfa3ff)
        await ctx.reply(embed=embed)

    def _get_created_at(self, user: discord.Member) -> str:
        return f'<t:{int(user.created_at.timestamp())}:d>'

    def _get_joined_at(self, user: discord.Member) -> str:
        return f'<t:{int(user.joined_at.timestamp())}:d>'

    def _get_joined_pos(self, user: discord.Member) -> str:
        members = sorted(user.guild.members, key=lambda m: m.joined_at)

        if user == user.guild.owner:
            join_pos_emoji = ":crown:"
        elif user == user.guild.me:
            join_pos_emoji = ":robot:"
        elif members.index(user) == 1:
            join_pos_emoji = ":second_place:"
        elif members.index(user) == 2:
            join_pos_emoji = ":third_place:"
        else:
            join_pos_emoji = ":white_small_square:"

        return f'{join_pos_emoji} {str(members.index(user) + 1)}'

    def _get_is_registered(self, user: discord.Member) -> bool:
        if self.db.users.find_one({"_id": user.id}):
            return True
        else:
            return False

    def _get_is_registered_str(self, user: discord.Member) -> str:
        if self.db.users.find_one({"_id": user.id}):
            return "Yes"
        else:
            return "No"

    def _get_balance(self, user: discord.Member) -> str:
        if self.db.users.find_one({"_id": user.id}):
            return f"{numerize.numerize(self.db.users.find_one({'_id': user.id})['balance'])} {settings.CURRENCY}"
        else:
            return "N/A"

    @user.command(
        name="infos",
        aliases=["ui", "info"],
        usage=">user infos [user]"
    )
    async def infos(self, ctx: commands.Context, user: discord.Member = None):
        """Get user info"""
        if user is None:
            user = ctx.message.author

        if user == self.bot.user:
            await ctx.reply(content="**Hey that's me!**", embed=HezaBot.embed())
            return

        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="Joined", value=self._get_joined_at(user))
        embed.add_field(name="Join position", value=self._get_joined_pos(user), inline=True)
        embed.add_field(name="Created", value=self._get_created_at(user))
        if not user.bot:
            embed.add_field(name="Registered", value=self._get_is_registered_str(user), inline=True)
            embed.add_field(name="Balance", value=self._get_balance(user), inline=True)
        else:
            embed.add_field(name="Bot", value="Yes", inline=True)
        embed.add_field(name="Status", value=user.status, inline=True)

        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
        else:
            embed.add_field(name="Roles", value="None", inline=False)

        if not self._get_is_registered(user):
            embed.add_field(name="Tips", value=f"Use `{settings.COMMAND_PREFIX}user register` to register yourself!")

        embed.set_footer(text=f'ID: {str(user.id)}')

        await ctx.reply(embed=embed)

    @user.command(
        name="list",
        aliases=["ls"],
        usage=">user list [qty]"
    )
    async def list(self, ctx: commands.Context, qty: int = 5) -> None:
        """List users"""
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        members = members[:qty]

        msg = ""

        for i, member in enumerate(members):
            if member == ctx.guild.owner:
                join_pos_emoji = ":crown:"
            elif member.bot:
                join_pos_emoji = ":robot:"
            elif i == 0:
                join_pos_emoji = ":first_place:"
            elif i == 1:
                join_pos_emoji = ":second_place:"
            elif i == 2:
                join_pos_emoji = ":third_place:"
            else:
                join_pos_emoji = ":white_small_square:"  # FIXME: found a way to just use a space (' ' & " " don't work)

            msg += f'{join_pos_emoji} {i + 1}. {member.mention}\n'

        embed = discord.Embed(title=f"Top {qty} members", description=msg, color=0xdfa3ff)
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(User(bot))
