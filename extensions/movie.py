import os
import datetime
import hikari
import lightbulb
import requests
import dotenv
from urllib.parse import quote
import random

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
@lightbulb.command("watch", "Start a watch party activity for the movie.", auto_defer=True, ephemeral=True)
@lightbulb.implements(lightbulb.PrefixSubCommand, lightbulb.SlashSubCommand)
async def watch_movie(ctx: lightbulb.Context) -> None: 
    # Retrieve the user's voice state from the cache.
    voice_state = ctx.bot.cache.get_voice_state(ctx.guild_id, ctx.member.id)
    if voice_state is None or voice_state.channel_id is None:
        await ctx.respond("You need to be in a voice channel to start a watch party.", reply=True)
        return

    # Search TMDb for the movie.
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
    movie_title = movie_result.get("title", "Unknown Title")
    mv_id = movie_result.get("id")
    if not mv_id:
        await ctx.respond("Movie ID not found.", reply=True)
        return

    # Retrieve the movie poster image if available.
    poster_path = movie_result.get("poster_path")
    poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

    # Build the external watch link.
    watch_link = f"https://2embed.top/embed/movie/{mv_id}"

    # Attempt to create an invite with Discord's Watch Together activity.
    discord_activity_invite = None
    try:
        invite = await ctx.bot.rest.create_invite(
            channel=voice_state.channel_id,
            max_age=86400,  # Invite valid for 24 hours.
            target_application_id=880218394199220334,  # Official Watch Together application ID.
            target_type=2  # Indicates an embedded activity.
        )
        discord_activity_invite = f"https://discord.com/invite/{invite.code}"
    except Exception as e:
        print(f"Error creating activity invite: {e}")

    # Build the embed description.
    description = ""
    if discord_activity_invite:
        description += f"**Join the Discord activity:** [Click here]({discord_activity_invite})\n\n"
    else:
        description += "Discord activity invite could not be created. "
    description += f"**Watch directly using this link:** [Watch Movie]({watch_link})\n\n"

    # Create the embed.
    embed = hikari.Embed(
        title=f"Watch Party for {movie_title.upper()}",
        description=description,
        colour=hikari.Color(0xe5e5e5),
        timestamp=datetime.datetime.now().astimezone(),
    )
    embed.set_footer(text=f"Requested by {ctx.member.display_name}", icon=ctx.member.avatar_url)
    
    # Use a thumbnail so the poster appears on the right.
    if poster_url:
        embed.set_thumbnail(poster_url)
        
    # Define a list of fun notes and select one at random.
    notes = [
        "So grab your popcorn, start sharing your screen, and let the movie marathon begin—have a blast together!",
        "Lights, camera, action! Share your screen and enjoy a blockbuster night!",
        "Popcorn? Check. Screen share? Check. Let’s dive into an epic movie adventure!",
        "Get ready for movie magic! Share your screen and enjoy every thrilling moment!",
        "Time for a cinematic treat! Share your screen and let the fun times roll!"
    ]
    random_note = random.choice(notes)
    
    # Add the random note as an embed field to make it more noticeable.
    embed.add_field(name=" ", value=random_note, inline=False)
    
    await ctx.respond(embed, reply=True)


# 2. movie similarities – provides similar movies the one requested 
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
