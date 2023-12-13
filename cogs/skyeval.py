#  ______     __  __     __  __     ______     ______
# /\  ___\   /\ \/ /    /\ \_\ \   /\  ___\   /\  == \
# \ \___  \  \ \  _--.  \ \____ \  \ \___  \  \ \  __<
#  \/\_____\  \ \_\ \_\  \/\_____\  \/\_____\  \ \_____\
#   \/_____/   \/_/\/_/   \/_____/   \/_____/   \/_____/
#
#                    AGPL-3.0 license

import ast
import utils

from discord.ext import commands as skySB


def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])
        if isinstance(body[-1], ast.If):
            insert_returns(body[-1].body)
            insert_returns(body[-1].orelse)
        if isinstance(body[-1], ast.With):
            insert_returns(body[-1].body)


async def execute_python_code(code, env={}):
    try:
        fn_name = "_eval_expr"
        cmd = "\n".join(f" {i}" for i in code.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)
        env = {'__import__': __import__, **env}
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
        return (await eval(f"{fn_name}()", env))
    except Exception as error:
        return error


class Eval(skySB.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.langpack = utils.Langs.getcurrent()['eval']

    @skySB.command(
        aliases=["eval", "py3", "python", "py"],
        description=utils.Langs.getcurrent()['eval']['e']['description'],
        usage="eval <code>"
    )
    async def e(self, ctx, *, code: str = None) -> None:
        if code:
            if code.startswith("```") and code.endswith("```"):
                code = "\n".join(code.split("\n")[1:])[:-3]

            result = await execute_python_code(
                code,
                {
                    'self': self,
                    'client': self.bot,
                    'bot': self.bot,
                    'app': self.bot,
                    'utils': utils,
                    'os': __import__('os'),
                    'discord': __import__('discord'),
                    'code': code,
                    'ctx': ctx,
                    'message': ctx.message
                }
            )
            if getattr(result, 'stringify', ''):
                try:
                    result = str(result.stringify())
                except:
                    pass

            await utils.answer(
                ctx,
                f"{self.langpack['e']['code']}"
                f"```py\n{code}\n```\n"
                f"{self.langpack['e']['result']}"
                f"```py\n{result}\n```"
            )
        else:
            await utils.answer(ctx, utils.Langs.getcurrent()['argRequired'].format('code'))


async def setup(bot) -> None:
    await bot.add_cog(Eval(bot))
