from discord.ext import commands
from requests import request
from json import loads
import discord
import settings
import random
import time

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loading_time = time.time()

        self.username = settings.IMGFLIP_USERNAME
        self.password = settings.IMGFLIP_PASSWORD

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
        '''Meme commands'''
        pass
        
    @meme.command(
            name="template", 
            usage=">meme template <qty>"
            )
    async def get_template(self, ctx: commands.Context, qty: int) -> None:
        '''Get a list of meme templates from imgflip'''
        req = request("GET", "https://api.imgflip.com/get_memes")

        self.data = loads(req.text)["data"]["memes"]
        random_memes = random.sample(self.data, qty)  # Select <qty> random memes
        msgs = [f'> `{i["id"]}` {i["name"]}  *(Texts: {i["box_count"]})*' for i in random_memes]
        msg = '\n'.join(msgs)

        await ctx.reply(f'**Here are {qty} random memes templates for you!**\n{msg}')

    @meme.command(
            name="create", 
            usage=">meme create <template_id> <text_fields>"
            )
    async def get_memes(self, ctx: commands.Context, template_id: str, text_fields: str) -> None:
        '''Generate a meme using imgflip
        > **Note:** Text field have to be in double quotes *(e.g. "text1")*
        > **Note:** Text fields have to be separated by `; ` *(e.g. "text1; text2")*'''
        try:
            params = {
                "template_id": template_id,
                "username": self.username,
                "password": self.password
            }
            
            # Split the text_fields string into individual text fields
            text_fields_list = text_fields.split('; ')

            for i, text in enumerate(text_fields_list):
                params[f"boxes[{i}][text]"] = text

            # Print full URL
            url = "https://api.imgflip.com/caption_image"

            req = request("GET", url, params=params)

            meme_url = loads(req.text)["data"]["url"]

            embed = discord.Embed(
                title="Here's your meme!",
                url=meme_url,
                description=f"**Template ID:** `{template_id}`"
            )

            embed.set_image(url=meme_url)
            embed.set_footer(text=f"Requested by {ctx.message.author.name}", icon_url=ctx.message.author.avatar)

            await ctx.reply(embed=embed)

        except Exception as e:
            await ctx.reply(f'**Error:** {e}')

async def setup(bot):
    await bot.add_cog(Memes(bot))