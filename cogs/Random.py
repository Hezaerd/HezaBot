from discord.ext import commands
from asyncio import TimeoutError
import discord
import random
import time

class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.loading_time = time.time()

        self.rps_reactions = [':rock:', ':roll_of_paper:', ':scissors:']

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f'Random cog loaded in {round(time.time() - self.loading_time, 2)} seconds')

    @commands.hybrid_group(
            name="random", 
            aliases=["rand"], 
            usage=">random [subcommand]", 
            invoke_without_command=True)
    async def random(self, ctx: commands.Context) -> None:
        '''Random commands'''
        pass

    @random.command(
            name="int", 
            usage=">random int <min> <max>")
    async def randint(self, ctx: commands.Context, min: int, max: int) -> None:
        '''Generates a random integer between min and max'''
        await ctx.reply(f'Result: {random.randint(min, max)}')

    @random.command(name="choose", 
                    aliases=["choice"], 
                    usage=">random choose <choice1; choice2; ...>")
    async def choose(self, ctx: commands.Context, choices: str) -> None:
        '''Chooses between multiple choices
        > **Note:** Choices have to be separated by `; ` *(e.g. "choice1; choice2")*'''
        choices = choices.split('; ')
        if not all(isinstance(choice, str) for choice in choices):
            await ctx.reply('**All choices have to be strings!**')
            return
        
        await ctx.reply(f'**Choice:** {random.choice(choices)}')

    @random.command(name="flip", 
                    aliases=["coinflip"], 
                    usage=">random flip [head/tail]")
    async def coinflip(self, ctx: commands.Context, prediction: str = None) -> None:
        ''':coin: Flips a coin'''
        result = random.choice(["Head", "Tail"])

        if prediction is not None and prediction.lower() not in ["head", "tail"]:
            await ctx.reply('**Invalid prediction!**')
            return

        if prediction is None:
            await ctx.reply(f':coin: {result} !')
        else:
            if prediction.lower() == result.lower():
                await ctx.reply(f':coin: {result} !\n**You won!**')
            else:
                await ctx.reply(f':coin: {result} !\n**You lost!**')

    @random.command(name="roll", 
                    aliases=["dice"], 
                    usage=">roll <NdN>")
    async def roll(self, ctx: commands.Context, dice: str) -> None:
        ''':game_die: Rolls a dice in NdN format'''
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.reply('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.reply(f':game_die: **{dice}**\n**Result:** {result}')

    @random.command(name="8ball", 
                    aliases=["8b"], 
                    usage=">random 8ball <question>")
    async def eightball(self, ctx: commands.Context, question: str) -> None:
        ''':crystal_ball: Ask the magic 8ball a question'''
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now...',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good...',
            'Very doubtful.'
        ]
        await ctx.reply(f'**Question:** {question}\n:crystal_ball: **Answer:** {random.choice(responses)}')

async def setup(bot):
    await bot.add_cog(Random(bot))