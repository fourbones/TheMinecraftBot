import json
from typing import Any

import discord
from discord import app_commands
from discord.ext import commands

from CodeUtils import embeds

bot_owner_id = 0
server_ip = ""
server_rcon_port = 25575
server_rcon_password = ""
server_member_role_name = ""
embed_title = ""
server_port = 25565


def _to_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def config_reload():
    global server_ip, server_rcon_port, server_rcon_password
    global server_member_role_name, embed_title, server_port, bot_owner_id

    with open('config.json', 'r', encoding='utf-8') as config_file:
        config = json.load(config_file)

    bot_owner_id = _to_int(config.get("bot_owner_id"), 0)
    server_ip = str(config.get("server_ip", ""))
    server_rcon_port = _to_int(config.get("server_rcon_port"), 25575)
    server_rcon_password = str(config.get("server_rcon_password", ""))
    server_member_role_name = str(config.get("server_member_role_name", ""))
    embed_title = str(config.get("embed_title", ""))
    server_port = _to_int(config.get("server_port"), 25565)


class setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        config_reload()

    @app_commands.command(name="mc-setup", description="this command lets you configure the bot")
    async def mcsetup(self, interaction: discord.Interaction):
        config_reload()
        if interaction.user.id == bot_owner_id:
            await interaction.response.send_modal(SetupModal())
        else:
            await interaction.response.send_message(embed=embeds.NotOwner(), ephemeral=True)


class SetupModal(discord.ui.Modal):
    def __init__(self):
        config_reload()
        super().__init__(title="Config")

        self.new_server_ip = discord.ui.TextInput(
            label="server_ip",
            default=str(server_ip),
            style=discord.TextStyle.short,
            placeholder="mc.yourdomain.de",
        )
        self.new_server_rcon_port = discord.ui.TextInput(
            label="server_rcon_port",
            default=str(server_rcon_port),
            style=discord.TextStyle.short,
            placeholder="default: 25575",
        )
        self.new_server_rcon_password = discord.ui.TextInput(
            label="server_rcon_password",
            default=str(server_rcon_password),
            style=discord.TextStyle.short,
            placeholder="Password",
        )
        self.new_server_member_role_name = discord.ui.TextInput(
            label="server_member_role_name",
            default=str(server_member_role_name),
            style=discord.TextStyle.short,
            placeholder="MC-Member",
        )
        self.new_server_port = discord.ui.TextInput(
            label="server_port",
            default=str(server_port),
            style=discord.TextStyle.short,
            placeholder="default: 25565",
        )

        for input_field in (
            self.new_server_ip,
            self.new_server_rcon_port,
            self.new_server_rcon_password,
            self.new_server_member_role_name,
            self.new_server_port,
        ):
            self.add_item(input_field)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_rcon_port = int(self.new_server_rcon_port.value)
            new_server_port = int(self.new_server_port.value)
        except ValueError:
            await interaction.response.send_message(
                "Bitte gib gültige Zahlen für die Ports ein.",
                ephemeral=True,
            )
            return

        with open('config.json', 'r', encoding='utf-8') as config_file:
            config = json.load(config_file)

        config.update(
            {
                "server_ip": self.new_server_ip.value.strip(),
                "server_rcon_port": new_rcon_port,
                "server_rcon_password": self.new_server_rcon_password.value.strip(),
                "server_member_role_name": self.new_server_member_role_name.value.strip(),
                "server_port": new_server_port,
            }
        )

        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(config, file, indent=4)

        config_reload()
        await interaction.response.send_message(embed=embeds.ConfigChanged(), ephemeral=True)

