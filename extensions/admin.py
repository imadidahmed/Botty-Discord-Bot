import lightbulb
import hikari




plugin = lightbulb.Plugin("admin")


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command(name="shutdown",description="shutdown the bot from the server", aliases=["sh"],ephemeral=True,hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def shutdown(ctx: lightbulb.Context) -> None:
    await ctx.bot.close()


@plugin.command
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("extension","extension group command",hidden=True)
@lightbulb.implements(lightbulb.PrefixCommandGroup)
async def ext(ctx:lightbulb.Context) -> None:
    await ctx.respond("load/unload/reload")


@ext.child
@lightbulb.option("extension","its an extension(obviously)")
@lightbulb.command("load","it loads an extension ",inherit_checks=True,hidden=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def loadext(ctx:lightbulb.Context) -> None:
    plugin.bot.load_extensions(f"extensions.{ctx.options.extension}")
    await ctx.respond("extension loaded succesfully")


@ext.child
@lightbulb.option("extension","its an extension(obviously)")
@lightbulb.command("unload","it unloads an extension ",inherit_checks=True,hidden=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def unloadext(ctx:lightbulb.Context) -> None:
    plugin.bot.unload_extensions(f"extensions.{ctx.options.extension}")
    await ctx.respond("extension unloaded succesfully")


@ext.child
@lightbulb.option("extension","its an extension(obviously)")
@lightbulb.command("reload","it reloads an extension",inherit_checks=True,hidden=True)
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def unloadext(ctx:lightbulb.Context) -> None:
    plugin.bot.reload_extensions(f"extensions.{ctx.options.extension}")
    await ctx.respond("extension reloaded succesfully")


@plugin.command
@lightbulb.command("server","num of servers")
@lightbulb.implements(lightbulb.PrefixCommand)
async def server (ctx : lightbulb.Context) -> None:
    await ctx.respond(f"Botty is in {len(plugin.bot.cache.get_guilds_view())} server.")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
