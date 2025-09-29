import datetime
import json

import discord
from discord.ext import commands

from CodeUtils import embeds
import mccommands
import setup
import mcrcon

from data_store import load_user_data, save_user_data

bot_token = None
server_ip = None
server_rcon_port = None
server_rcon_password = None
server_member_role_name = None


def config_reload():
    global bot_token, server_ip, server_rcon_port, server_rcon_password, server_member_role_name
    with open('config.json', 'r') as config:
        config = json.load(config)
    bot_token = str(config["bot_token"])
    server_ip = str(config["server_ip"])
    server_rcon_port = int(config["server_rcon_port"])
    server_rcon_password = str(config["server_rcon_password"])
    server_member_role_name = config["server_member_role_name"]


config_reload()
load_user_data()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(mccommands.mccommands(bot))
    await bot.add_cog(setup.setup(bot))

    print(f'Logged in as {bot.user.name}')
    with open('config.json', 'r') as file:
        config_data = json.load(file)

    config_data['bot_name'] = bot.user.name

    with open('config.json', 'w') as file:
        json.dump(config_data, file, indent=4)

    print(f"|✅|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - All Cogs Loaded")

    await bot.tree.sync()
    print(f"|✅|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - bot.tree synced")



@bot.event
async def on_member_update(before, after):
    if server_member_role_name in [role.name for role in after.roles]:
        if server_member_role_name not in [role.name for role in before.roles]:
            await set_mcname_permission(after, True)
            await notify_role_added(after)

    if server_member_role_name not in [role.name for role in after.roles]:
        if server_member_role_name in [role.name for role in before.roles]:
            await set_mcname_permission(after, False)
            await remove_from_whitelist(after)


async def remove_from_whitelist(member):
    config_reload()
    data = load_user_data()

    discord_name = str(member)
    record = data.get(discord_name)
    if not record:
        return

    minecraft_name = record.get("minecraft_name", "")
    if not minecraft_name:
        return

    rcon = mcrcon.MCRcon(host=str(server_ip), password=str(server_rcon_password), port=int(server_rcon_port))
    try:
        rcon.connect()
        rcon.command(f'whitelist remove {minecraft_name}')
        rcon.command(f'kick {minecraft_name} Du bist nicht mehr auf der Whitelist!')
        print(f"|🖥|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - removed {minecraft_name} from the whitelist")
    finally:
        try:
            rcon.disconnect()
        except Exception:
            pass

    record["minecraft_name"] = ""
    record["permission"] = False
    data[discord_name] = record
    save_user_data(data)


async def notify_role_added(member):
    try:
        await member.send(embed=embeds.MCaddUserEmbed())
    except discord.Forbidden:
        print(
            f"|⚠️|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - "
            f"Could not DM {member}: DMs are disabled."
        )
    except discord.HTTPException as exc:
        print(
            f"|⚠️|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - "
            f"Failed to DM {member}: {exc}"
        )


def is_mcname_permission_allowed(member):
    data = load_user_data()

    discord_name = str(member)
    if discord_name in data:
        return data[discord_name].get("permission", False)

    return False


async def set_mcname_permission(member, permission):
    data = load_user_data()

    discord_name = str(member)
    record = data.get(discord_name, {"minecraft_name": "", "permission": False})
    record["permission"] = permission
    data[discord_name] = record
    save_user_data(data)

bot.run(str(bot_token))
