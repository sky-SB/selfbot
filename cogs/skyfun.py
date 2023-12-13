#  ______     __  __     __  __     ______     ______    
# /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \   
# \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<   
#  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
#   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#   
#                    AGPL-3.0 license

import random

import discord
from discord.ext import commands as skySB
import utils

class Fun(skySB.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langpack = utils.Langs.getcurrent()['fun']
        
    @skySB.command(
        description=utils.Langs.getcurrent()['fun']['dick']['description']
    )
    async def dick(self, ctx, user: discord.User = None):
        if user:
            mention = user.mention
        else:
            mention = self.bot.user
            
        size = random.randint(1, 1000)
        await utils.answer(
            ctx, 
            self.langpack['dick']['text'].format(mention, size))

    @skySB.command(
        description=utils.Langs.getcurrent()['fun']['iq']['description']
    )
    async def iq(self, ctx, user: discord.User = None):
        if user:
            mention = user.mention
        else:
            mention = self.bot.user
            
        iq = random.randint(1, 1000)
        await utils.answer(
            ctx, 
            self.langpack['iq']['text'].format(mention, iq))
            
    @skySB.command(
        description=utils.Langs.getcurrent()['fun']['gay']['description']
    )
    async def gay(self, ctx, user: discord.User = None):
        if user:
            mention = user.mention
        else:
            mention = self.bot.user
            
        percent = random.randint(0, 101)
        await utils.answer(
            ctx, 
            self.langpack['gay']['text'].format(mention, percent))
            
async def setup(bot):
    await bot.add_cog(Fun(bot))