import datetime
import setup
import discord
from discord.ext import commands
from discord import  app_commands
from CodeUtils import embeds
import json
import mcrcon

bot_owner_id = None
server_ip = None
server_rcon_port = None
server_rcon_password = None
server_member_role_name = None
bot_name = None

def config_reload():
    global server_ip, server_rcon_port, server_rcon_password, server_member_role_name, bot_name, bot_owner_id
    with open('config.json', 'r') as config:
        config = json.load(config)
    bot_owner_id = int(config["bot_owner_id"])
    server_ip = config["server_ip"]
    server_rcon_port = config["server_rcon_port"]
    server_rcon_password = config["server_rcon_password"]
    server_member_role_name = config["server_member_role_name"]
    bot_name = config["bot_name"]

class mccommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    config_reload()

    @app_commands.command(name="mc-setname",description="this command connects your Minecraft account to your Discord account")
    async def mcsetname(self, interaction: discord.Interaction, mcname: str):
        config_reload()
        try:
            discord_name = str(interaction.user.name)
            if is_mcname_permission_allowed(discord_name):
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


async def save_to_json(discord_name, minecraft_name):
    data = {}
    try:
        with open('user_data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        pass

    data[discord_name] = {"minecraft_name": minecraft_name, "permission": True}

    with open('user_data.json', 'w') as file:
        json.dump(data, file, indent=4)


async def add_to_whitelist(discord_name, minecraft_name):
    config_reload()
    rcon = mcrcon.MCRcon(host=str(server_ip), password=str(server_rcon_password), port=int(server_ip))
    rcon.connect()
    rcon.command(f'whitelist add {minecraft_name}')
    rcon.disconnect()



def is_mcname_permission_allowed(member):
    with open('user_data.json', 'r') as file:
        data = json.load(file)

    discord_name = str(member)
    if discord_name in data:
        return data[discord_name]["permission"]

    return False

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelpGithubButton("GitHub",discord.ButtonStyle.url,None, "https://github.com/fourbones/TheMinecraftBot"))
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
