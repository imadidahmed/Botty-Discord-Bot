import asyncio
import hikari
import lightbulb



plugin = lightbulb.Plugin("random")

@plugin.command
@lightbulb.command(name="ping",description="pong",aliases=["pg"],auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommand,lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    await asyncio.sleep(1)
    await ctx.respond(f"Latency: {int(plugin.bot.heartbeat_latency*1000)} ms",reply=True, mentions_reply=True)



def load(bot:lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)