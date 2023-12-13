#  ______     __  __     __  __     ______     ______    
# /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \   
# \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<   
#  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
#   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#   
#                    AGPL-3.0 license

import aiohttp
import os
import re
import subprocess
import sys

from discord.ext import commands as skySB
import utils


class Loader(skySB.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langpack = utils.Langs.getcurrent()['loader']

    @skySB.command(
        aliases=["lm", "install", "le"],
        description=utils.Langs.getcurrent()['loader']['loadExt']['description']
    )
    async def loadExt(self, ctx, *, url: str = None):
        await utils.answer(ctx, self.langpack['loadExt']['wait'].format(url))
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                text = await resp.text()

        name_search = re.search(r'# name: (\w+)', text)
        if name_search:
            name = name_search.group(1)
        else:
            return await utils.answer(ctx, utils.Langs.getcurrent()['error'].format('необходимо указать name в коге!'))

        requirements_search = re.search(r'# requirements: (\w+)', text)
        if requirements_search:
            requirements = requirements_search.group(1)
            await utils.answer(ctx, self.langpack['loadExt']['libwait'])
            try:
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pip",
                        "install",
                        "--user",
                        *requirements
                    ], 
                check=True)
            except subprocess.CalledProcessError as error:
                return await utils.answer(ctx, utils.Langs.getcurrent()['error'].format(error))

        with open(f"cogs/{name}.py", "a") as f:
            f.write(text)
        await self.bot.load_extension(f"cogs.{name}")
        await utils.answer(ctx, self.langpack['loadExt']['done'])

    @skySB.command(
        aliases=["reload", "rl", "reloadcogs"],
        description=utils.Langs.getcurrent()['loader']['reloadExt']['description']
    )
    async def reloadExt(self, ctx):
        msg = ''
        msg += self.langpack['reloadExt']['title']
        for file in os.listdir(f"cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.bot.reload_extension(f"cogs.{extension}")
                    msg += self.langpack['reloadExt']['format'].format(extension)
                except:
                    pass
                    
        await utils.answer(ctx, msg)


async def setup(bot):
    await bot.add_cog(Loader(bot))