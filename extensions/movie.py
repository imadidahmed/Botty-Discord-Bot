import os
import datetime
import hikari
import lightbulb
import requests
import dotenv
from urllib.parse import quote

# Load environment variables; MOVIE_API_KEY should be your TMDb Bearer token
dotenv.load_dotenv()
TMDB_BEARER = os.environ.get("MOVIE_API_KEY")
if not TMDB_BEARER:
    raise ValueError("MOVIE_API_KEY (Bearer token) not set in environment.")

base_url = "https://api.themoviedb.org/3"

# Headers as recommended by TMDb when using Bearer token authentication
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_BEARER}"
}

# Use a persistent session for efficiency
session = requests.Session()

plugin = lightbulb.Plugin("movie")

@plugin.command()
@lightbulb.add_cooldown(5.0, 3, lightbulb.UserBucket)
@lightbulb.command("movie", "Movie command that helps you search for movies.", auto_defer=True)
@lightbulb.implements(lightbulb.PrefixCommandGroup, lightbulb.SlashCommandGroup)
async def movie(ctx: lightbulb.Context) -> None:
    ...

# 1. Search for a movie and show its details
@movie.child
@lightbulb.add_cooldown(5.0, 3, lightbulb.UserBucket)
@lightbulb.option("movie", "The title of the movie to search for.")
@lightbulb.command("search", "Retrieve detailed information about a movie.", aliases=["src"])
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def search_movie(ctx: lightbulb.Context) -> None:
    query = ctx.options.movie
    # Use parameters as a dict and include language
    params_search = {"query": query, "language": "en-US"}
    search_url = f"{base_url}/search/movie"
    r1 = session.get(search_url, headers=headers, params=params_search)
    if r1.status_code != 200:
        await ctx.respond("Failed to retrieve movie data from TMDb.", reply=True)
        return

    data = r1.json()
    if not data.get("results"):
        await ctx.respond("No movie found with that title.", reply=True)
        return

    movie_result = data["results"][0]
    mv_id = movie_result.get("id")
    if not mv_id:
        await ctx.respond("Movie ID not found in search results.", reply=True)
        return

    # Retrieve detailed movie data and appended videos
    params_details = {"append_to_response": "videos", "language": "en-US"}
    details_url = f"{base_url}/movie/{mv_id}"
    r2 = session.get(details_url, headers=headers, params=params_details)
    if r2.status_code != 200:
        await ctx.respond("Failed to retrieve movie details.", reply=True)
        return
    data2 = r2.json()

    # Extract video information if available
    video_key = None
    if data2.get("videos") and data2["videos"].get("results"):
        video_results = data2["videos"]["results"]
        if video_results:
            video_key = video_results[0].get("key")

    # Extract common fields
    title = movie_result.get("title", "Unknown Title")
    overview = movie_result.get("overview", "No overview available.")
    release_date = movie_result.get("release_date", "")
    release_year = release_date[:4] if release_date else "N/A"
    poster_path = movie_result.get("poster_path")
    image = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    rating = data2.get("vote_average", "N/A")
    runtime = data2.get("runtime", "N/A")
    status_movie = data2.get("status", "N/A")
    genres = "  ".join([g.get("name") for g in data2.get("genres", []) if g.get("name")]) or "N/A"

    embed = hikari.Embed(
        title=f"{title.upper()} ({release_year})",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    if image:
        embed.set_thumbnail(image)
    embed.add_field(name="OVERVIEW", value=overview)
    embed.add_field(name="GENRES", value=genres, inline=True)
    embed.add_field(name="RATING", value=str(rating), inline=True)
    embed.add_field(name="DURATION", value=f"{runtime} min", inline=True)
    embed.add_field(name="STATUS", value=status_movie, inline=True)
    if video_key:
        embed.add_field(name="Trailer", value=f"https://www.youtube.com/watch?v={video_key}", inline=False)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed, reply=True, mentions_reply=True)

# 2. Watch a movie – provides a link to an external embed service
@movie.child
@lightbulb.add_cooldown(5.0, 3, lightbulb.UserBucket)
@lightbulb.option("movie", "The title of the movie you want to watch.")
@lightbulb.command("watch", "Get a link to watch the movie.", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def watch_movie(ctx: lightbulb.Context) -> None:
    query = ctx.options.movie
    params_search = {"query": query, "language": "en-US"}
    search_url = f"{base_url}/search/movie"
    r1 = session.get(search_url, headers=headers, params=params_search)
    if r1.status_code != 200:
        await ctx.respond("Failed to retrieve movie data from TMDb.", reply=True)
        return
    data = r1.json()
    if not data.get("results"):
        await ctx.respond("No movie found with that title.", reply=True)
        return

    movie_result = data["results"][0]
    title = movie_result.get("title", "Unknown Title")
    mv_id = movie_result.get("id")
    if not mv_id:
        await ctx.respond("Movie ID not found.", reply=True)
        return

    poster_path = movie_result.get("poster_path")
    image = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    # Example: using an external embed service
    watch_link = f" https://2embed.top/embed/movie/{mv_id}"
    embed = hikari.Embed(
        title=f"🎬 WATCH [{title.upper()}] NOW",
        url=watch_link,
        timestamp=datetime.datetime.now().astimezone(),
        colour=hikari.Color(0xe5e5e5),
    )
    if image:
        embed.set_image(image)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed, reply=True)

# 3. Trending movies this week (uses /trending/movie/week)
@movie.child
@lightbulb.add_cooldown(5.0, 3, lightbulb.UserBucket)
@lightbulb.command("trending", "Show trending movies this week.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def trending_movies(ctx: lightbulb.Context) -> None:
    params = {"language": "en-US", "page": 1}
    trending_url = f"{base_url}/trending/movie/week"
    r = session.get(trending_url, headers=headers, params=params)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve trending movies.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No trending movies found.", reply=True)
        return

    movies_list = [movie.get("title", "Unknown") for movie in data.get("results", [])]
    embedlist = "\n".join(movies_list)
    first_result = data["results"][0]
    poster_path = first_result.get("poster_path")
    thumbnail = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    embed = hikari.Embed(
        title="TRENDING MOVIES",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    if thumbnail:
        embed.set_thumbnail(thumbnail)
    embed.add_field(name="TRENDING MOVIES THIS WEEK", value=embedlist)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed, reply=True)

# 4. Similar movies for a given movie
@movie.child
@lightbulb.add_cooldown(5.0, 3, lightbulb.UserBucket)
@lightbulb.option("movie", "The title of the movie for which to find similar movies.")
@lightbulb.command("similar", "Get similar movies to a given movie.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def similar_movies(ctx: lightbulb.Context) -> None:
    query = ctx.options.movie
    params_search = {"query": query, "language": "en-US"}
    search_url = f"{base_url}/search/movie"
    r1 = session.get(search_url, headers=headers, params=params_search)
    if r1.status_code != 200:
        await ctx.respond("Failed to retrieve movie data from TMDb.", reply=True)
        return
    data1 = r1.json()
    if not data1.get("results"):
        await ctx.respond("No movie found with that title.", reply=True)
        return

    movie_result = data1["results"][0]
    mv_id = movie_result.get("id")
    if not mv_id:
        await ctx.respond("Movie ID not found.", reply=True)
        return

    params_similar = {"language": "en-US"}
    similar_url = f"{base_url}/movie/{mv_id}/similar"
    r = session.get(similar_url, headers=headers, params=params_similar)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve similar movies.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No similar movies found.", reply=True)
        return

    similar_movies_list = [movie.get("title", "Unknown") for movie in data.get("results", [])]
    embedlist = "\n".join(similar_movies_list)
    poster_path = movie_result.get("poster_path")
    image = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    original_title = movie_result.get("original_title", "Unknown")
    embed = hikari.Embed(
        title="SIMILAR MOVIES",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    embed.add_field(name=f"Similar to {original_title.upper()}:", value=embedlist)
    if image:
        embed.set_thumbnail(image)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed, reply=True)

# 5. Popular movies (uses /movie/popular)
@movie.child
@lightbulb.add_cooldown(5.0, 3, lightbulb.UserBucket)
@lightbulb.command("popular", "Get a list of popular movies right now.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def popular_movies(ctx: lightbulb.Context) -> None:
    params = {"language": "en-US", "page": 1}
    popular_url = f"{base_url}/movie/popular"
    r = session.get(popular_url, headers=headers, params=params)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve popular movies.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No popular movies found.", reply=True)
        return

    popular_movies_list = [movie.get("title", "Unknown") for movie in data.get("results", [])]
    popular_movies_str = "\n".join(popular_movies_list)
    poster_path = data["results"][0].get("poster_path")
    image = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    embed = hikari.Embed(
        title="POPULAR MOVIES",
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone()
    )
    embed.add_field(name="A LIST OF POPULAR MOVIES", value=popular_movies_str)
    if image:
        embed.set_thumbnail(image)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed, reply=True)

# 6. Recommended movies for a given movie
@movie.child
@lightbulb.add_cooldown(5.0, 3, lightbulb.UserBucket)
@lightbulb.option("movie", "The title of the movie for which to get recommendations.")
@lightbulb.command("recommendation", "Get movie recommendations based on a given movie.")
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def recommendation(ctx: lightbulb.Context) -> None:
    query = ctx.options.movie
    params_search = {"query": query, "language": "en-US"}
    search_url = f"{base_url}/search/movie"
    r1 = session.get(search_url, headers=headers, params=params_search)
    if r1.status_code != 200:
        await ctx.respond("Failed to retrieve movie data from TMDb.", reply=True)
        return
    data1 = r1.json()
    if not data1.get("results"):
        await ctx.respond("No movie found with that title.", reply=True)
        return

    movie_result = data1["results"][0]
    mv_id = movie_result.get("id")
    if not mv_id:
        await ctx.respond("Movie ID not found.", reply=True)
        return

    params_rec = {"language": "en-US"}
    rec_url = f"{base_url}/movie/{mv_id}/recommendations"
    r = session.get(rec_url, headers=headers, params=params_rec)
    if r.status_code != 200:
        await ctx.respond("Failed to retrieve recommendations.", reply=True)
        return
    data = r.json()
    if not data.get("results"):
        await ctx.respond("No recommendations found.", reply=True)
        return

    rec_movies_list = [movie.get("title", "Unknown") for movie in data.get("results", [])]
    embedlist = "\n".join(rec_movies_list)
    poster_path = movie_result.get("poster_path")
    image = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
    original_title = movie_result.get("original_title", "Unknown")
    embed = hikari.Embed(
        title="MOVIE RECOMMENDATIONS".upper(),
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone()
    )
    embed.add_field(name=f"Recommendations based on {original_title.upper()}:", value=embedlist)
    if image:
        embed.set_thumbnail(image)
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    await ctx.respond(embed, reply=True)

def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)

def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
