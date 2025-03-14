import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))  # Convert to int
ALLOWED_ROLE_IDS = [1121590212011773962, 1091441098330746919]

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="bke!", intents=intents)

# Slash Commands
async def setup_hook():
    bot.tree.copy_global_to(guild=discord.Object(id=GUILD_ID))
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

bot.setup_hook = setup_hook

@bot.tree.command(name="ping")
@app_commands.guilds(discord.Object(id=GUILD_ID))
async def ping(interaction: discord.Interaction):
    ping = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! Latency is {ping}ms.")

@bot.tree.command(name="say")
@app_commands.guilds(discord.Object(id=GUILD_ID))
@app_commands.describe(channel="The channel to send the message to", message="The message to send")
async def say(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    if any(role.id in ALLOWED_ROLE_IDS for role in interaction.user.roles):
        await channel.send(message)
        await interaction.response.send_message("Message sent!", ephemeral=True)
    else:
        await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    print(f"Guild ID: {GUILD_ID}")
    print("Slash commands should be available in a few minutes.")
    await bot.change_presence(activity=discord.Game(name="BKBot but extra"))

# Run the bot
bot.run(TOKEN)
