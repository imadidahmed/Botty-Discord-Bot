# Botty Discord Bot


Botty is a versatile Discord bot developed by me using Python and powered by the Hikari and Lightbulb libraries. The bot provides users with comprehensive information about movies and series, including popular and trending titles. It also features a powerful search functionality for finding specific movies & series. Each entry in the bot's responses is enriched with its title, a brief description, genres, release date, actors, and the movie/serie thumbnail.

## Features

- **Movie and Series Information:** Botty can provide detailed information about various movies and series. Just ask for details about your favorite movie/serie!

- **Popular and Trending:** Stay up-to-date with the latest popular and trending movies and series. Botty can fetch this information for you effortlessly.

- **Search Functionality:** Looking for a specific movie or series? Botty's got you covered! Search for your desired content using keywords.

- **Similar Movies and Series:** Discover similar movies and series to the one you're interested in. Botty can recommend movies & series that share thematic or genre similarities.

- **Comprehensive Details:** Each entry provided by Botty includes:
  - **Title:** The title of the movie or series.
  - **Description:** A concise description to give you an idea of the content.
  - **Genres:** The genres the content falls under.
  - **Release Date:** The date when the movie or series was released.
  - **Actors:** The notable actors who star in the content.
  - **Thumbnail:** A thumbnail image to visually represent the movie/serie.

## Getting Started

### Prerequisites

- Python 3.6+
- Git

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/imadidahmed/Botty-Discord-Bot.git
   cd botty-discord-bot

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt

3. **Configure the Bot:**

    Create a new Discord bot on the Discord Developer Portal.
    Copy the bot token.
    Rename config.example.json to config.json and replace YOUR_BOT_TOKEN with the actual bot token.

4. **Run the Bot:**

    ```bash
    python bot.py

5. **Invite Botty to Your Server:**
    Generate an OAuth2 URL for your bot using the Discord Developer Portal.
    Visit the generated URL and select your server to invite Botty.

## Usage

- Use the `!help` command to get a list of available commands and their descriptions.

### Examples

- `!movie Avengers`: Get information about the movie "Avengers."
- `!series Stranger Things`: Get information about the series "Stranger Things."
- `!popular_movies`: Get a list of popular movies.
- `!trending_series`: Get a list of trending series.
- `!search Sci-Fi`: Search for movies and series with the keyword "Sci-Fi."

## Contributing

Contributions to Botty are welcome! If you'd like to enhance the bot's features or fix issues, please create pull requests.

## Support

If you encounter any issues or have questions about using Botty, join our [support server](https://discord.gg/xAbsk6Fz) for assistance.

---

Enjoy using Botty to explore movies and series, and have a great time in your Discord server! If you have any suggestions or feedback, we'd love to hear from you. Happy watching! 🍿🎬
