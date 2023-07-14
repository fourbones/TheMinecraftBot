from CodeUtils import embeds
import json, discord, datetime
from discord.ext import commands
from discord import  app_commands

bot_owner_id = None
server_ip = None
server_rcon_port = None
server_rcon_password = None
server_member_role_name = None
embed_title = None
server_port = None



def config_reload():
    global server_ip, server_rcon_port, server_rcon_password, server_member_role_name, embed_title, server_port, bot_owner_id
    with open('config.json', 'r') as config:
        config = json.load(config)
    bot_owner_id = int(config["bot_owner_id"])
    server_ip = str(config["server_ip"])
    server_rcon_port = int(config["server_rcon_port"])
    server_rcon_password = str(config["server_rcon_password"])
    server_member_role_name = config["server_member_role_name"]
    embed_title = config["embed_title"]
    server_port = str(config["server_port"])


class setup(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    config_reload()

    @app_commands.command(name="mc-setup",description="this command lets you configure the bot")
    async def mcsetup(self, interaction: discord.Interaction):
        config_reload()
        if interaction.user.id == bot_owner_id:
            await interaction.response.send_modal(SetupModal())
        else:
            await interaction.response.send_message(embed=embeds.NotOwner())

class SetupModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Config")

    new_server_ip = discord.ui.TextInput(label="server_ip", default=str(server_ip), style=discord.TextStyle.short, placeholder="mc.yourdomain.de")
    new_server_rcon_port = discord.ui.TextInput(label="server_rcon_port", default=str(server_rcon_port), style=discord.TextStyle.short, placeholder="default: 25575")
    new_server_rcon_password = discord.ui.TextInput(label="server_rcon_password", default=str(server_rcon_password), style=discord.TextStyle.short, placeholder="Password")
    new_server_member_role_name = discord.ui.TextInput(label="server_member_role_name", default=str(server_member_role_name), style=discord.TextStyle.short, placeholder= "MC-Member")
    new_server_port = discord.ui.TextInput(label="server_port", default=str(server_port), style=discord.TextStyle.short, placeholder="default: 25565")


    async def on_submit(self, interaction: discord.Interaction):
        with open('config.json', 'r') as config:
            config = json.load(config)

        config["server_ip"] = self.new_server_ip
        config["server_rcon_port"] = int(self.new_server_rcon_port)
        config["server_rcon_password"] = self.new_server_rcon_password
        config["server_member_role_name"] = self.new_server_member_role_name
        config["server_port"] = int(self.new_server_port)

        with open('config.json.json', 'w') as file:
            json.dump(config, file, indent=4)

        await interaction.response.send_message(embed= embeds.ConfigChanged())