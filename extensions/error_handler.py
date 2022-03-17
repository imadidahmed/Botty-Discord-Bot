import hikari
import lightbulb



plugin = lightbulb.Plugin("err_handler")

@plugin.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    if isinstance(event.exception,lightbulb.CommandNotFound):
        await event.context.respond("Command does not exist. Check the help.")
    if isinstance(event.exception, lightbulb.NotEnoughArguments):
        await event.context.respond("This command should have arguments.")
    if isinstance(event.exception, lightbulb.CommandIsOnCooldown):
        await event.context.respond(f"This command is in cooldown please repeat later.")
    if isinstance(event.exception, lightbulb.CommandInvocationError):
        await event.context.respond(f"Something went wrong during the call of the {event.context.command.name} command.")
    if isinstance(event.exception,lightbulb.ExtensionAlreadyLoaded):
        await event.context.respond("This extension already loaded.")
    if isinstance(event.exception,lightbulb.ExtensionNotLoaded):
        await event.context.respond("This extension is not loaded.")
    if isinstance(event.exception,lightbulb.ExtensionNotFound):
        await event.context.respond("This extension is not found or missing.")
    if isinstance(event.context,lightbulb.CommandIsOnCooldown):
        await event.context.respond("this command is in cooldown repeat after 5 sec !!!")
    if isinstance(event.exception,lightbulb.NotOwner):
        await event.context.respond("You can't use this type of commands (OWNER ONLY).")

    

    
    raise event.exception



def load(bot:lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)