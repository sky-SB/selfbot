![logo](https://cdn.discordapp.com/attachments/1067827666885034106/1181891500330713098/-1_orig.jpg)
<p align="center">
    </a>
    <br>
    <b>☄️ sky selfbot</b>
    <br>
    <b>best open source selfbot for discord!</b>
    <br>
</p>

<h1>Installing</h1>
<pre lang="bash">
git clone https://github.com/sky-sb/selfbot.git
cd selfbot
pip install -r requirements.txt
</pre>

<h1>Starting</h1>
<pre lang="bash">
python3 skySB.py
</pre>

<h1>Custom cogs/modules</h1>
<pre lang="python">
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
</pre>

<h1>Links</h1>
<a href='https://discord.gg/'>Official discord server</a>