import datetime
import json
from typing import Any

import discord
from discord import app_commands
from discord.ext import commands

from CodeUtils import embeds
import mcrcon
import setup

from data_store import load_user_data, save_user_data

bot_owner_id = None
server_ip = None
server_rcon_port = None
server_rcon_password = None
server_member_role_name = None
bot_name = None


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def config_reload():
    global server_ip, server_rcon_port, server_rcon_password, server_member_role_name, bot_name, bot_owner_id
    with open('config.json', 'r') as config:
        config = json.load(config)
    bot_owner_id = _to_int(config.get("bot_owner_id"), 0)
    server_ip = config.get("server_ip", "")
    server_rcon_port = _to_int(config.get("server_rcon_port"), 25575)
    server_rcon_password = config.get("server_rcon_password", "")
    server_member_role_name = config.get("server_member_role_name", "")
    bot_name = config.get("bot_name", "")

class mccommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    config_reload()

    @app_commands.command(name="mc-setname",description="this command connects your Minecraft account to your Discord account")
    async def mcsetname(self, interaction: discord.Interaction, mcname: str):
        config_reload()
        try:
            discord_name = str(interaction.user)
            if is_mcname_permission_allowed(discord_name):
                await check_json(discord_name)
                await save_to_json(discord_name, mcname)
                print(f"|🗄|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - saved DC: {discord_name} MC: {mcname} to json")
                await add_to_whitelist(discord_name, mcname)
                print(f"|🖥|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - added {mcname} to whitelist")
                await interaction.response.send_message(embed=embeds.MCWhitelistaddEmbed())
            else:
                await interaction.response.send_message(embed=embeds.MCNotAllowed())
        except Exception as e:
            await interaction.response.send_message(embed=embeds.MCError())
            print(f"|❌|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - {e}")

    @app_commands.command(name="mc-help", description="this will return some help hopefully.")
    async def mchelp(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=embeds.Help(), view = HelpView())

    @app_commands.command(name="mc-status", description="Shows the Minecraft name linked to your Discord account.")
    async def mcstatus(self, interaction: discord.Interaction):
        discord_name = str(interaction.user)
        data = load_user_data()
        record = data.get(discord_name, {})
        minecraft_name = record.get("minecraft_name")
        allowed = record.get("permission", False)

        await interaction.response.send_message(
            embed=embeds.MCStatusEmbed(minecraft_name, allowed),
            ephemeral=True,
        )

async def check_json(discord_name):
    config_reload()
    data = load_user_data()
    record = data.get(discord_name)

    if not record:
        return

    minecraft_name = record.get("minecraft_name", "")
    if minecraft_name != "":
        print(f"|🔍|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - Checked Json File and deleted the old {minecraft_name} from the whitelist")
        rcon = mcrcon.MCRcon(host=str(server_ip), password=str(server_rcon_password), port=int(server_rcon_port))
        try:
            rcon.connect()
            rcon.command(f'whitelist remove {minecraft_name}')
            rcon.command(f'kick {minecraft_name} Du bist nicht mehr auf der Whitelist!')
        finally:
            try:
                rcon.disconnect()
            except Exception:
                pass
        record["minecraft_name"] = ""
        data[discord_name] = record
        save_user_data(data)
    else:
        print(f"|🔍|{datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')}| - Checked Json File and no old user name was found")



async def save_to_json(discord_name, minecraft_name):
    data = load_user_data()
    record = data.get(discord_name, {"minecraft_name": "", "permission": True})
    record["minecraft_name"] = minecraft_name
    record["permission"] = True
    data[discord_name] = record
    save_user_data(data)


async def add_to_whitelist(discord_name, minecraft_name):
    config_reload()
    rcon = mcrcon.MCRcon(host=str(server_ip), password=str(server_rcon_password), port=int(server_rcon_port))
    try:
        rcon.connect()
        rcon.command(f'whitelist add {minecraft_name}')
    finally:
        try:
            rcon.disconnect()
        except Exception:
            pass



def is_mcname_permission_allowed(member):
    data = load_user_data()

    if member in data:
        return data[member].get("permission", False)

    return False

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpGithubButton("GitHub",discord.ButtonStyle.url,None, "https://4bones.de"))
        self.add_item(HelpGithubButton("Wiki", discord.ButtonStyle.url, None, "https://github.com/fourbones/TheMinecraftBot/wiki"))
        self.add_item(HelpGithubButton("Setup", discord.ButtonStyle.green, "⚙️", None))

class HelpGithubButton(discord.ui.Button):
    def __init__(self, Buttonname, Buttonstyle, emoji, url):
        super().__init__(label=Buttonname, style=Buttonstyle, emoji=emoji, url=url)
        self.Name = Buttonname

    async def callback(self, interaction: discord.Interaction):
        config_reload()
        if self.Name == "Setup" and int(interaction.user.id) == int(bot_owner_id):
            await interaction.response.send_modal(setup.SetupModal())
        else:
            await interaction.response.send_message(embed=embeds.NotOwner())
