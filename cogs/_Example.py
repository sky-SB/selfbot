# name: Example

import utils
from discord.ext import commands as skySB

class Example(skySB.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
    @skySB.command(description='hi')
    async def example(self, ctx) -> None:
        await utils.answer(ctx, 'Hello!')

async def setup(bot) -> None:
    await bot.add_cog(Example(bot))