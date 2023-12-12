from discord.ext import commands
from requests import request
from json import loads
import discord
import env
import random

class Memes(commands.Cog, name="Memes"):
    def __init__(self, bot):
        self.bot = bot

        self.username = env.IMGFLIP_USERNAME
        self.password = env.IMGFLIP_PASSWORD

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Memes cog loaded')
        
    @commands.hybrid_command(name="memetemplate")
    async def get_template(self, ctx, qty: int):
        '''Get a list of meme templates'''
        ''' Use: >memetemplate <qty>'''
        req = request("GET", "https://api.imgflip.com/get_memes")

        self.data = loads(req.text)["data"]["memes"]
        random_memes = random.sample(self.data, qty)  # Select <qty> random memes
        msgs = [f'> `{i["id"]}` {i["name"]}  *(Texts: {i["box_count"]})*' for i in random_memes]
        msg = '\n'.join(msgs)

        await ctx.reply(f'**Here are {qty} random memes templates for you!**\n{msg}')

    @commands.hybrid_command(name="meme")
    async def get_memes(self, ctx, template_id: str, text_fields: str):
        '''Get a meme'''
        ''' Use: >meme <template_id> <text_fields>'''
        '''e.g. >meme 181913649 "Hello;World;This is a meme"'''
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