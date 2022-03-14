import asyncio
import datetime
import random 
import hikari
import lightbulb
import wikipedia

plugin=lightbulb.Plugin("wikipedia")

wiki_icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAhFBMVEX///8AAAD8/Pz29vaOjo75+fnz8/OUlJTw8PCsrKxqamqfn5/d3d3m5ubo6Ojr6+u4uLhWVlYwMDB1dXWlpaXV1dW+vr6KiopSUlJvb2/IyMgcHBw1NTXZ2dmYmJjCwsJiYmIpKSlERESAgIAPDw89PT3Ozs4iIiIYGBg0NDRISEhTU1Pvn3jFAAAIuklEQVR4nO2c6XbqOgyFKWEsQ0sLhdP2QChDh/P+73cJltNke5ADZFjr6vsHiGDHtrYkO7RagiAIgiAIgiAIgiAIgiAIgiAIgiAIgiAIgiAIgiAIgiAIgiAIgiAIglAdx2Wn01+v54+vfx8Gg6ib+agd9QaD6WLzOByt+51OZzlO3p0mX+iPhpuTfa8L1uPjS2Lc7yw35zcfl6eLj4Yvi+mgF7W1aTexfH2cJ1ftn98ZJhc92R1Pdt2s3fSozNbt1oW0D3dZ3r5/ZnF8fyKe/Ry2+9yHd3HyjWX2nS2Zx7PVYZs3TmzH2Tc+D6vzlWc/T9nrJrdtmrvmx8xid7y0h73Pu3AOyTfuA42T4R0G2C1Odkfe7PXSHgY3OGHWCmx1QmL7Emg3Ya32XV8nvESd2YG9fsJ2Fav7OIo/ONunVbxOTLu7eLX12H3PntXs68f/njxm/3aTizuY0H44Lplevo/Gvcw3Hl53btvnzSR7w6PJ3H5Hnh9zdt3J0Go3m08uH78si9jd5v3GtI/6dttdz7RtPZp2ozC71eImvVOMXZNv5rDfWmyHdltcaM+OYUE7x+Uuxj4sHy7zyPTDjpuBo+NueM437f9e2SGTua2H7kU+Nmwfnbb7IKtWa5uxu30HT37S7OC9x9xQjhenacY1jXwt6IRc7Br+GD2c+8xnYOyefr8r4I+3Ab83bXdZDzi6b9hDix/9BT2Dcx3+9nDrjzDTBft2cSTK8Bo+8RKWYB25DNNZyrj/YdjvXgOGcX2/eeg0/Qq7XDrW7tlwNTjxfvzm4Gxc0qKveuB+Xt/gWyo9ggGZPyRsb/PWjhygH9pwsosvaHgw03yTOZ8Gg+iYXSSHfj96YlHBELZaz9BFf+DbhqTA2jYdStiC0Ry7oKVxLbgSvQptDOLKYtKlqezV1rOhf67fDEgznhhlghtiGcR52IXSu8X6o2vBogIjTRDNmisxok988aiC0tRbpxQmkEcxq6LNDeIydGQo3Ph0xg03AzNRxrOt89YxfNyj9/lyGS0PLiq4AZj5+fKLEwOoOkLWQ775H/uz2sU9XNH0UDAXZn6zk7eOcx/qLHLM/ipJxfPl7Q7nAXrIqD6a5zpzH9rutu3bpYF5IrP2IdKLMx/pKIWvB5JPtglqCfyFHjJaPXAP4ixoFiRQcFS22mt+8k3mxBoivV/XpPNNXgA2yrB0tYffS2FUHyO9dBDf1es1/4skFeWrPYEBNbc6IHHWfoWUdc+XJMjlvpWv9hqsLDKlPVy4yrHo+xQwMOSsKlB7Dco4o/oYrqtMcB68tnTsOri+5cFgrs/8Nobr09N7EVXuAqpK8+yNqQisaHcYewjXk5VIAatzXyAD3Ytq1F4D5d494wNwECfpzAuozpPrLrHCZgObzGXosAe50/M8pNl0N6tSe813vskHxuXjnra+QwEzj1ZEZWqvwY0Xb4G/ZQwiEZIq0GhXpvaaCDYxONW3bPXeBWV7FNZ+Vaf2Gsj7uPmG1eEznAtOmIeb3hiMNjm1su2whowLzZUq1V6D2zTcjDM7yJZIW6lUVKr2Gow2uXlk7CG/hfzKKmgNlMQ7NJiZcxH2kC+RplJRsdpr0D1y/hx9E7tR0UqlgtOisoC6IqfJWM4ISIYewq5cGriyuLgKt735E1vzsNlRGlgo5FQfdx/58sU29FaUBe4mch6v2O5jKhU1qL0G00QuzCw6iFTUq0PtNStoMqf6ECUwG0l0A2tRew3WFTn3iIPuj2poUpdxhC0cEAxudw9905dvJZK61KT2GkwTGb9uHI3zDSKJUV1qT/SgrujXZsupdLcx1VO/b9ziwqCKe1XfcpraPeibkKVaATgsPtW3PTrx6bQmP13WMcRwcFw8e4F44tQ7iOR2a1R7DQ6MW/WNw5tn3h2DRFJRxb49Bz7u4WwTFb7hdIYjTaRDGrWqvQbTRFcoRiXTJWbOT1Zrug/1qj3RBsH4dKg4BQeRoaG2QaTSHH8KpRLw+Il92lG/RqfWQ6l1a7GmAS/vuHMhMBR7txnRMfjznj8WFi23ZOXsey1g2mc7wjXKdgbszUCI6ni1q71mAS22xMqROq1Ou4XoTo3Qk+5Z2Q0PB46fWHL9fm50sbCIBxzp82X5LQ8F00TjCFAPBhedE0SzNMZNUHsNCMYe6w47GFt0TrASlVdqhNprsK4Ix7+nxtDiUYeccyKpKPdMfkFwYX3mg80/xqzDmlTuwIJa1hWd0gsFxyQncZQm5Io4qDCZlUiuuSFqr8ESU071VYUt/1C558k21Xl34lgTmPtlFhHJNySCuP2YrkQqQDVG7TWY/GXGRC0rjMBw1FFJ6s/tEUwTU2U4GgtNgcUBPerqVYPUXoM5USoNKvE18yAsDpDvpHTzuj9KKAdosN5tcIsbbgmobFfdEO60Yy3gFq9S/bbK6G3xCQ5inLy5cN6Q+kERV+6eJu/U9g08J5UMogoOSn4C71LQ/58lW2VN9tP4GLDfpwFrw9Reg2liovoUsDpKN1CTOvlfJRX7SttdAEwTF/qpSJd6Y5nuvuW3rx2zwWpInlx7aG04w3lH3qr6U3qhQHvvjipvdB8Nsv/tUgPVXmP5c5A771HutvXPtpqo9kTP1l7v05O2E4uNVHsNZn0J/l3qgnekdsz/3eHmHBYWw55PqBFzi5B59M44sdhUtddgmMKXBDGcbazaa9A5sgcQMZxl/qWhfkDhAh69gyJWc9WegL8YCDg3mR/EBqu9Jnf8xL6/C+SOEdVzoLsQuTJh0Hmm7Dficht3GzJpYuCRtMw3GpnbI8fC7f19rqG2A93FSIsTwQFmWlgMeUChAaRpYvD+nx72rzKbdUuKO34qLDY2t0eoLl9Au9WegLGx2ljU3kqh8Ou8J1DS/z2WQZIm8n9tleUcsTc4t0ceZl8/BYOT9faz8TF3jpCntvJEjQ+5BUEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEEQBEH4n/AfSYJdaU8dAWsAAAAASUVORK5CYII="


@plugin.command
@lightbulb.command(name="wiki",description="wiki group command",auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommandGroup,lightbulb.SlashCommandGroup)
async def wiki(ctx:lightbulb.Context) -> None: 
    await asyncio.sleep(1)
    await ctx.respond("I need a subcommand.Check the subcommands using a SlashPrefix before me.")

@wiki.child
@lightbulb.option(name="target",description="target to search for")
@lightbulb.command(name="search",description="it gives you search results",aliases=["sea","src","srch"])
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def summary(ctx: lightbulb.Context) -> None:
    search = wikipedia.search(ctx.options.target,results=10,suggestion=True)
    
    results=[]
    for i in range(len(search[0])):
        results.append(search[0][i])
    results="\n".join(results)
    
    embed =(hikari.Embed(
        title="Search Result:",
        description=results,
        timestamp=datetime.datetime.now().astimezone(),
        colour= hikari.Color(0x7f9c85),
    )   
        .set_thumbnail(wiki_icon)
        .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)
    )
    await ctx.respond(embed,reply=True,mentions_reply=True)


@wiki.child
@lightbulb.option(name="target",description="target to search for")
@lightbulb.command(name="summary",description="it gives you a summary",aliases=["sum","su","smry"])
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def summary(ctx: lightbulb.Context) -> None:
    summary = wikipedia.summary(ctx.options.target,chars=2000, redirect=True)
    embed =(hikari.Embed(
        title=(ctx.options.target).upper(),
        description=summary,
        timestamp=datetime.datetime.now().astimezone(),
        colour= hikari.Color(0x7f9c85),
    )   
        .set_thumbnail(wiki_icon)
        .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)
    )
    await ctx.respond(embed,reply=True,mentions_reply=True)

@wiki.child
@lightbulb.command(name="random",description="it gives you random topics",aliases=["rand","r","rnd"])
@lightbulb.implements(lightbulb.PrefixSubCommand,lightbulb.SlashSubCommand)
async def summary(ctx: lightbulb.Context) -> None:
    randommy = random.choice(wikipedia.random(pages=5))
    summary = wikipedia.summary(randommy,chars=2000,auto_suggest=True,redirect=True)
    embed =(hikari.Embed(
        title=f"Topic you may like ({randommy.upper()}):",
        description=summary,
        timestamp=datetime.datetime.now().astimezone(),
        colour= hikari.Color(0x7f9c85),
    )
        .set_thumbnail(wiki_icon)
        .set_footer(f"Requested by {ctx.member.display_name}",icon=ctx.member.avatar_url)
    )
    await ctx.respond(embed,reply=True,mentions_reply=True)



def load(bot:lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)