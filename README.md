# Discord Minecraft Whitelist Bot

## Description

This is a small Discord bot that allows you to easily manage your Minecraft server whitelist. With this bot, adding someone to your whitelist is as simple as giving them a specific role on your Discord server. The bot can be easily configured through the `config.json` file or directly using the `/mc-setup` command in Discord. It utilizes mcrcon for server communication.

## Setup

1. Download the bot.
2. Open the `config.json` file and enter your Discord bot token and ID.
3. Install the required dependencies by running `pip install -r requirements.txt`.
4. Start the bot and add it to your Discord server.
5. Type the command `/mc-setup` in a text channel that the bot can read, or send the bot a direct message.
6. Fill out all the requested information provided by the bot and click "Done".
7. You're done! It's that easy.

## How to Use

To add a user to the Minecraft server whitelist, simply assign them the configured role on your Discord server. The bot will prompt the user for their Minecraft name, and once provided, it will add the user to the Minecraft server whitelist. If you remove the assigned role from a user, the bot will automatically remove them from the Minecraft server whitelist and kick them if they are currently online.

