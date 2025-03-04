import os
import datetime
import hikari
import lightbulb
import requests
import dotenv
from urllib.parse import quote

plugin = lightbulb.Plugin("serie")
dotenv.load_dotenv()

base_url = "https://api.themoviedb.org/3"
# MOVIE_API_KEY now stores your Bearer token (do not pass it as a query parameter)
BEARER_TOKEN = os.environ.get("MOVIE_API_KEY")
if not BEARER_TOKEN:
    raise ValueError("MOVIE_API_KEY (Bearer token) not set in environment.")

# Set headers as recommended by TMDb for Bearer token authentication
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# Use a persistent session for efficiency
session = requests.Session()

# Register the command group properly with a Context parameter
@plugin.command()
@lightbulb.command("serie", "Commands for TV show-related queries.", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def serie(ctx: lightbulb.Context) -> None:
    pass

# 1. Search for a TV show and display its details
@serie.child
@lightbulb.option("name", "The name of the TV show you want to search for.")
@lightbulb.command("search", "Retrieve detailed information about a TV show.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def search_show(ctx: lightbulb.Context) -> None:
    params_search = {
        "query": ctx.options.name,
        "language": "en-US"
    }
    search_url = f"{base_url}/search/tv"
    r = session.get(search_url, headers=headers, params=params_search)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve TV show data from TMDb.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No TV show found with that name.", reply=True)
        return

    show_result = data["results"][0]
    serie_id = show_result.get("id")
    if not serie_id:
        await ctx.respond("TV show ID not found.", reply=True)
        return

    params_details = {"language": "en-US"}
    details_url = f"{base_url}/tv/{serie_id}"
    r2 = session.get(details_url, headers=headers, params=params_details)
    if r2.status_code != 200:
        await ctx.respond("Failed to retrieve TV show details.", reply=True)
        return
    data2 = r2.json()

    num_of_episodes = data2.get("number_of_episodes", "N/A")
    num_of_seasons = data2.get("number_of_seasons", "N/A")
    overview = data2.get("overview", "No overview available.")
    serie_title = data2.get("original_name", "Unknown Title")
    rating = data2.get("vote_average", "N/A")
    first_air_date = data2.get("first_air_date", "")
    year = first_air_date[:4] if first_air_date else "N/A"
    episode_run_time = data2.get("episode_run_time", [])
    duration = episode_run_time[0] if episode_run_time else "N/A"
    status_show = data2.get("status", "N/A")
    poster_path = data2.get("poster_path")
    poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    creators_list = [creator.get("name") for creator in data2.get("created_by", []) if creator.get("name")]
    creators = " - ".join(creators_list) if creators_list else "Unknown"

    genres_list = [genre.get("name") for genre in data2.get("genres", []) if genre.get("name")]
    genres = "  ".join(genres_list) if genres_list else "N/A"

    embed = hikari.Embed(
        title=f"{serie_title.upper()} ({year})",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone()
    )
    if poster:
        embed.set_thumbnail(poster)
    embed.add_field(name="OVERVIEW", value=overview)
    embed.add_field(name="GENRES", value=genres, inline=True)
    embed.add_field(name="RATING", value=str(rating), inline=True)
    embed.add_field(name="STATUS", value=status_show, inline=True)
    embed.add_field(name="SEASONS", value=f"{num_of_seasons} season(s)", inline=True)
    embed.add_field(name="EPISODES", value=f"{num_of_episodes} episode(s)", inline=True)
    embed.add_field(name="DURATION", value=f"{duration} min", inline=True)
    embed.add_field(name="CREATORS", value=creators)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed, reply=True)

# 2. Watch a chosen episode from a TV show
@serie.child
@lightbulb.option("name", "The name of the TV show you want to watch.")
@lightbulb.option("season_number", "Season number.", type=int)
@lightbulb.option("episode_number", "Episode number.", type=int)
@lightbulb.command("watch", "Watch a chosen episode from your TV show.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def watch(ctx: lightbulb.Context) -> None:
    params_search = {"query": ctx.options.name, "language": "en-US"}
    search_url = f"{base_url}/search/tv"
    r = session.get(search_url, headers=headers, params=params_search)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve TV show data from TMDb.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No TV show found with that name.", reply=True)
        return
    show_result = data["results"][0]
    serie_id = show_result.get("id")
    if not serie_id:
        await ctx.respond("TV show ID not found.", reply=True)
        return

    # Optionally retrieve season data for further validation if needed
    params_season = {"language": "en-US"}
    season_url = f"{base_url}/tv/{serie_id}/season/{ctx.options.season_number}"
    r_season = session.get(season_url, headers=headers, params=params_season)
    if r_season.status_code != 200:
        await ctx.respond("Failed to retrieve season data.", reply=True)
        return

    # Construct a watch link using an external embed service (example)
    watch_link = f"https://multiembed.mov?video_id={serie_id}&tmdb=1&s={ctx.options.season_number}&e={ctx.options.episode_number}"
    serie_title = show_result.get("original_name", "Unknown Title")
    poster_path = show_result.get("poster_path")
    poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    embed = hikari.Embed(
        title=f"WATCH {serie_title.upper()} S{ctx.options.season_number} E{ctx.options.episode_number}",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
        url=watch_link
    )
    if poster:
        embed.set_image(poster)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed)

# 3. Top rated TV shows
@serie.child
@lightbulb.command("top_rated", "Get a list of the top rated TV shows.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def top_rated(ctx: lightbulb.Context) -> None:
    params = {"language": "en-US", "page": 1}
    top_url = f"{base_url}/tv/top_rated"
    r = session.get(top_url, headers=headers, params=params)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve top rated TV shows.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No top rated TV shows found.", reply=True)
        return

    series_names = []
    for item in data["results"]:
        name = item.get("original_name", "Unknown")
        vote = item.get("vote_average", "N/A")
        series_names.append(f"{name} ({vote})")
    series_names_str = "\n".join(series_names)
    poster_path = data["results"][0].get("poster_path")
    poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    embed = hikari.Embed(
        title="TOP RATED TV-SHOWS",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    embed.add_field(name="LIST OF TOP RATED TV-SHOWS", value=series_names_str)
    if poster:
        embed.set_thumbnail(poster)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed)

# 4. Popular TV shows
@serie.child
@lightbulb.command("popular", "Get a list of the current popular TV shows.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def popular(ctx: lightbulb.Context) -> None:
    params = {"language": "en-US", "page": 1}
    popular_url = f"{base_url}/tv/popular"
    r = session.get(popular_url, headers=headers, params=params)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve popular TV shows.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No popular TV shows found.", reply=True)
        return

    series_names = []
    for item in data["results"]:
        name = item.get("original_name", "Unknown")
        first_air_date = item.get("first_air_date", "")
        year = first_air_date[:4] if first_air_date else "N/A"
        series_names.append(f"{name} ({year})")
    series_names_str = "\n".join(series_names)
    poster_path = data["results"][0].get("poster_path")
    poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    embed = hikari.Embed(
        title="POPULAR TV-SHOWS",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    embed.add_field(name="LIST OF CURRENT POPULAR TV-SHOWS", value=series_names_str)
    if poster:
        embed.set_thumbnail(poster)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed)

# 5. Similar TV shows
@serie.child
@lightbulb.option("name", "The name of the TV show to find similar shows for.")
@lightbulb.command("similar", "Get a list of similar TV shows.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def similar_series(ctx: lightbulb.Context) -> None:
    params = {"query": ctx.options.name, "language": "en-US"}
    search_url = f"{base_url}/search/tv"
    r = session.get(search_url, headers=headers, params=params)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve TV show data from TMDb.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No TV show found with that name.", reply=True)
        return

    show_result = data["results"][0]
    serie_id = show_result.get("id")
    if not serie_id:
        await ctx.respond("TV show ID not found.", reply=True)
        return

    similar_url = f"{base_url}/tv/{serie_id}/similar"
    r2 = session.get(similar_url, headers=headers, params={"language": "en-US"})
    if r2.status_code != 200:
        await ctx.respond("Failed to retrieve similar TV shows.", reply=True)
        return
    data2 = r2.json()
    if not data2.get("results"):
        await ctx.respond("No similar TV shows found.", reply=True)
        return

    similar_names = [item.get("original_name", "Unknown") for item in data2.get("results", [])]
    similar_str = "\n".join(similar_names)
    poster_path = show_result.get("poster_path")
    poster = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    original_title = show_result.get("original_name", "Unknown")
    
    embed = hikari.Embed(
        title="SIMILAR TV-SHOWS",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    embed.add_field(name=f"TV-SHOWS LIKE {original_title.upper()}:", value=similar_str)
    if poster:
        embed.set_thumbnail(poster)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
