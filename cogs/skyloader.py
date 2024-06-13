#  ______     __  __     __  __     ______     ______
# /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \
# \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<
#  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
#   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#
#                    AGPL-3.0 license

import requests
import os
import re
import subprocess
import sys

from discord.ext import commands as skySB
from utils import *


class Loader(skySB.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langpack = langs.getcurrent()['loader']

    @skySB.command(
        aliases=["unlm", "uninstall", "unle"],
        description=langs.getcurrent()['loader']['unloadExt']['description']
    )
    async def unloadExt(self, ctx, *, name: str):
        await answer(ctx, self.langpack['unloadExt']['wait'].format(ext_name), delete=False)

        if os.path.exists(f"./cogs/{name}.py"):
            await answer(ctx, self.langpack['unloadExt']['errorsystem'])
            return

        if not os.path.exists(f"./modules/custom/{name}.py"):
            await answer(ctx, self.langpack['unloadExt']['notfound'])
            return

        await bot.unload_extension(f"cogs.custom.{name}")
        os.remove("./cogs/custom/{name}.py")

        await answer(ctx, self.langpack['unloadExt']['done'].format(name))

    @skySB.command(
        aliases=["lm", "install", "le"],
        description=langs.getcurrent()['loader']['loadExt']['description']
    )
    async def loadExt(self, ctx, *, url: str):
        ext_name = os.path.basename(url).split(".")[0]
        await answer(ctx, self.langpack['loadExt']['wait'].format(ext_name), delete=False)
        if not validators.Link(url):
            await answer(ctx, self.langpack['loadExt']['errorlink'])
            return

        resp = requests.get(url)
        if not resp.ok:
            await answer(ctx, self.langpack['loadExt']['errorresp'])
            return

        if os.path.exists(f"./cogs/custom/{ext_name}.py"):
            await answer(ctx, self.langpack['loadExt']['errorexists'])
            return

        with open(f"./cogs/custom/{ext_name}.py", "wb") as f:
            f.write(resp.content)

        await bot.load_extension(f"cogs.custom.{ext_name}")
        await answer(ctx, self.langpack['loadExt']['done'].format(ext_name))

    @skySB.command(
        aliases=["reload", "rl", "reloadcogs"],
        description=langs.getcurrent()['loader']['reloadExt']['description']
    )
    async def reloadExt(self, ctx):
        msg = ''
        msg += self.langpack['reloadExt']['title']
        for file in os.listdir(f"cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.bot.reload_extension(f"cogs.{extension}")
                    msg += self.langpack['reloadExt']['format'].format(
                        extension)
                except:
                    pass

        await answer(ctx, msg)


async def setup(bot):
    await bot.add_cog(Loader(bot))
