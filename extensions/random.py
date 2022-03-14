import asyncio
from aiohttp import request
import hikari
import lightbulb



plugin = lightbulb.Plugin("random")


@plugin.command
@lightbulb.command("kanye","it gives you random kanye quotes",aliases=["ye"],auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def kanye(ctx:lightbulb.Context) -> None:
    URL="https://api.kanye.rest/"
    async with request("GET",URL) as response:
        if response.status == 200:
            data=await response.json()
            quote=data["quote"]
            await ctx.respond(f"Ye once said: {quote}")


@plugin.command
@lightbulb.command("hello","it says hello")
@lightbulb.implements(lightbulb.PrefixCommand)
async def hello(ctx:lightbulb.Context) -> None:
    await ctx.respond(f"hello {ctx.member.display_name}")




def load(bot:lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)

