# Telegram Bot Request Logger

The Telegram Bot Request Logger is a Python-based Telegram bot that generates unique URLs for users and logs all incoming requests sent to these URLs. It provides a simple and efficient way to track and monitor HTTP requests.

## Install
git clone https://github.com/MrRage867/Request-Logger.git

## Bot Preview
[Request Logger Bot](https://t.me/RequestLoggingBot)

## Example
![Start logger](https://cdn.discordapp.com/attachments/846740705430208522/1115381302582071358/image.png)<br><br>
![Receive file](https://cdn.discordapp.com/attachments/846740705430208522/1115381335272472716/image.png)

## Features

- Generates unique URLs for each user to log HTTP requests.
- Logs incoming requests and saves them to individual log files.
- Retrieves the number of requests received and provides the log file upon request.
- Handles concurrent requests using threading.

## Usage

1. Start the Telegram bot by running the `bot.py` script.

2. Interact with the bot by sending commands through the Telegram chat interface.

   - Use the `/log` command followed by the desired logging duration in seconds to start logging requests. For example: `/log 60` will log requests for 60 seconds.
   - The bot will generate a unique URL for you to send requests to during the specified duration.
   - Once the logging duration is complete, the bot will provide the number of requests received and send you the log file.

## Contributors

This Telegram bot was developed by t.me/MrRage.
