import random
import time
from json import loads

import discord
from discord.ext import commands
from requests import request

import settings
from Modules import Colors


class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loading_time = time.time()

        self.username = settings.IMGFLIP_USERNAME
        self.password = settings.IMGFLIP_PASSWORD

        self.data = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Memes cog loaded in {round(time.time() - self.loading_time, 2)} seconds')

    @commands.hybrid_group(
        name="meme",
        aliases=["memes"],
        usage=">meme [subcommand]",
        invoke_without_command=True
    )
    async def meme(self, ctx: commands.Context) -> None:
        """Meme commands"""
        pass

    @meme.command(
        name="template",
        usage=">meme template <amount>"
    )
    async def get_template(self, ctx: commands.Context, amount: int = 5) -> None:
        """Get a list of meme templates from imgflip"""
        req = request("GET", "https://api.imgflip.com/get_memes")

        self.data = loads(req.text)["data"]["memes"]
        random_memes = random.sample(self.data, amount)  # Select <qty> random memes
        msgs = [f'> `{i["id"]}` {i["name"]}  *(Texts: {i["box_count"]})*' for i in random_memes]
        msg = '\n'.join(msgs)

        await ctx.reply(f'**Here are {amount} random memes templates for you!**\n{msg}')

    def _get_meme(self, template_id: str, text_fields: str) -> str:
        """Generate a meme using imgflip
        > **Note:** Text field have to be in double quotes *(e.g. "text1")*
        > **Note:** Text fields have to be separated by `; ` *(e.g. "text1; text2")*"""
        params = {
            "template_id": template_id,
            "username": self.username,
            "password": self.password
        }

        text_fields_list = self._split_text_fields(text_fields)

        for i, text in enumerate(text_fields_list):
            params[f"boxes[{i}][text]"] = text

        url = "https://api.imgflip.com/caption_image"

        req = request("GET", url, params=params)

        meme_url = loads(req.text)["data"]["url"]

        return meme_url

    # noinspection PyMethodMayBeStatic
    def _embed_meme(self, ctx: commands.Context,  template_id: str, meme_url: str) -> discord.Embed:
        embed = discord.Embed(
            title="Here's your meme!",
            url=meme_url,
            description=f"**Template ID:** `{template_id}`",
            color=Colors.Embed.random()
        )

        embed.set_image(url=meme_url)
        embed.set_footer(text=f"Requested by {ctx.message.author.name}", icon_url=ctx.message.author.avatar)

        return embed

    # noinspection PyMethodMayBeStatic
    def _concat_text_fields(self, *text_field: str) -> str:
        """Concatenate text fields into a single string"""
        return '; '.join(text_field)

    # noinspection PyMethodMayBeStatic
    def _split_text_fields(self, text_fields: str) -> list:
        """Split text fields into a list"""
        return text_fields.split('; ')

    @meme.command(
        name="create",
        usage=">meme create <template_id> <text_fields>"
    )
    async def get_meme(self, ctx: commands.Context, template_id: str, text_fields: str) -> None:
        """Generate a meme using imgflip
        > **Note:** Text field have to be in double quotes *(e.g. "text1")*
        > **Note:** Text fields have to be separated by `; ` *(e.g. "text1; text2")*"""

        try:
            meme_url = self._get_meme(template_id, text_fields)
            await ctx.reply(embed=self._embed_meme(ctx, template_id, meme_url))

        except Exception as e:
            await ctx.reply(f'**Error:** {e}')

    @meme.command(
        name="anakin",
        usage=">meme anakin"
    )
    async def meme_anakin(self, ctx: commands.Context, text_field1: str = "", text_field2: str = "",
                          text_field3: str = "") -> None:
        """Anakin with Padme meme"""
        template_id = "322841258"

        text_fields = self._concat_text_fields(text_field1, text_field2, text_field3)

        try:
            meme_url = self._get_meme(template_id, text_fields)
            await ctx.reply(embed=self._embed_meme(ctx, template_id, meme_url))

        except Exception as e:
            await ctx.reply(f'**Error:** {e}')


async def setup(bot):
    await bot.add_cog(Memes(bot))
