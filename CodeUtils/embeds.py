import discord
from discord.ext import commands
from datetime import datetime
import json

server_ip = None
server_rcon_port = None
server_rcon_password = None
server_member_role_name = None
embed_title = None
server_port = None
bot_name = None

def config_reload():
    global server_ip, server_rcon_port, server_rcon_password, server_member_role_name, embed_title, server_port, bot_name
    with open('config.json', 'r') as config:
        config = json.load(config)
    server_ip = config["server_ip"]
    server_rcon_port = config["server_rcon_port"]
    server_rcon_password = config["server_rcon_password"]
    server_member_role_name = config["server_member_role_name"]
    embed_title = config["embed_title"]
    server_port = str(config["server_port"])
    bot_name = config["bot_name"]


def MCWhitelistaddEmbed():
    config_reload()
    embed = discord.Embed(title=embed_title, color=discord.Color.green(),
                          description="Your Minecraft username has been saved, and you have been added to the whitelist! If you change your Minecraft username you can just simple use `/mc-setname` again to also update that name on the Minecraft server")
    embed.add_field(name="IP", value=f"`{server_ip}`")
    embed.add_field(name="Port",value=f"`{server_port}`")
    embed.set_footer(text=f"created by {bot_name} | {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
    return embed


def MCaddUserEmbed():
    config_reload()
    embed = discord.Embed(title=embed_title, color=discord.Color.green(),
                          description=f"Welcome to the Minecraft server! You are now officially part of it! To get on the whitelist, simply enter your Minecraft username using the command `/mc-setname`.")
    embed.set_footer(text=f"created by {bot_name} | {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
    return embed

def MCNotAllowed():
    config_reload()
    embed = discord.Embed(title=embed_title, color=discord.Color.red(),
                          description="You are not authorized to use this command!")
    embed.set_footer(text=f"created by {bot_name} | {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
    return embed

def MCError():
    config_reload()
    embed = discord.Embed(title=embed_title, color=discord.Color.red(),
                          description="An error occurred while trying to connect to the Minecraft server. This could be because the server is currently restarting or undergoing maintenance. You can try using this command again in a few minutes. If it still doesn't work, please contact the owner of the Discord server.")
    embed.set_footer(text=f"created by {bot_name} | {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
    return embed


def Help():
    config_reload()
    embed = discord.Embed(title=f"Help - {embed_title}", color=discord.Color.green(),
                          description="This is a bot written in Python that manages the members on your Minecraft Server. The bot was programmed by Fourbones and is an open-source project. You can find the GitHub repository below. The bot is quite simple—it waits for a role to be added to any Discord member on a Discord Server. Once the specified role, as defined in the configuration, is added, the bot will message that person and ask for their Minecraft Name. When the user provides their Minecraft Name, the bot will connect to your Minecraft Server via rcon and add the user to the whitelist. If the role is removed from a user, the bot will automatically remove the user from the whitelist and kick them if they are online. To Configure the bot use `/mc-setup`")
    embed.set_footer(text=f"created by {bot_name} | {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
    return embed

def NotOwner():
    config_reload()
    embed = discord.Embed(title=embed_title, color=discord.Color.red(),
                          description="You are not allowed to use this command. Only the bot owner has permission to use it. If you are the bot owner, you need to set your ID as the bot_owner_id in the config.json file.")
    embed.set_footer(text=f"created by {bot_name} | {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
    return embed

def ConfigChanged():
    config_reload()
    embed = discord.Embed(title=embed_title, color=discord.Color.green(),
                          description="The Config was saved")
    embed.set_footer(text=f"created by {bot_name} | {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
    return embed
