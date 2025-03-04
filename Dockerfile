# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot’s source code
COPY . .

# Set environment variables if needed (e.g., Discord token)
# You might also use a .env file and pass it in with docker-compose

# Command to run your bot
CMD ["python", "bot.py"]
