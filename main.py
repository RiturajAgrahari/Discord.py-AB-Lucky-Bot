import os
import sys
import datetime

import discord

from log import logger
from db import db_init
from models import BotUsage, Profile, TodayLuck

from discord.ext import tasks
from dotenv import load_dotenv
from discord import app_commands
from discord.errors import Forbidden

from luck import lucky_all_embeds
from embeds import help_embed, today_luck_embed
from review import review_area
from config import reset_data

from config import config_bot


# LOADING ENV
load_dotenv()

permitted_users = ['<@568179896459722753>']


# INITIALIZING
MY_GUILD = int(os.getenv("MY_GUILD"))
TEST_GUILD = int(os.getenv("TEST_GUILD"))
MAIN_GUILD = int(os.getenv("MAIN_GUILD"))
guilds = [MY_GUILD, TEST_GUILD, MAIN_GUILD]


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """
        Initializing guilds and connecting it to the bot.
        :return:
        """
        for guild in guilds:
            main_guild = discord.Object(id=guild)
            try:
                self.tree.copy_global_to(guild=main_guild)
                await self.tree.sync(guild=main_guild)
            except Forbidden:
                logger.error(f"GUILD ID : [{guild}] Bot has Missing Access")


intents = discord.Intents.default()
intents.message_content = True  # Allows bot to read messages (note: allow from discord application portal as well)
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await db_init()
    await reset_function.start()


# Last Optimization [11-11-2024]
@tasks.loop(minutes=1)
async def reset_function():
    # Get the current UTC time
    try:
        current_time_utc = datetime.datetime.utcnow().today()
    except Exception:
        current_time_utc = datetime.datetime.now(datetime.datetime.UTC)

    # Check if it's UTC 00:00
    # print(current_time_utc.hour, current_time_utc.minute)
    if current_time_utc.hour == 0 and current_time_utc.minute == 0:
        await reset_data(client)


# Last Optimization [11-11-2024]
@client.event
async def on_message(message):
    # Check if the message author is not client itself
    if message.author == client.user:
        pass

    elif message.channel.type == discord.ChannelType.private:
        print(f'DM --> [{message.author}] : {message.content}')

    # Message in server channels
    else:
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        guild_name = message.guild.name
        # print(f"[{channel}-----{username}------] : {user_message}")

        if message.author.mention in permitted_users:
            if user_message == "tommy!":
                await message.reply(content="wuff wuff!")

            elif user_message == "$config-lucky":
                await config_bot(message, client)


# Last Optimization [11-11-2024]
@client.tree.command(name='help', description='Shows help for the bot.')
async def help_command(interaction: discord.Interaction):
    if interaction.guild.id == MAIN_GUILD or interaction.user.mention in permitted_users:
        await add_bot_usage()
        avatar = await get_avatar(interaction)
        embed = await help_embed(interaction.user, avatar)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(
            embed=discord.Embed(title='',
                                description="This command is not available in this server.",
                                color=discord.Color.red()),
            ephemeral=True)


# Last Optimization [11-11-2024]
@client.tree.command(name="feedback", description="help us to improve")
async def feedback(interaction: discord.Interaction):
    if interaction.guild.id == MAIN_GUILD or interaction.user.mention in permitted_users:
        await add_bot_usage()
        user = await check_profile(interaction)
        await review_area(interaction, user, client)
    else:
        await interaction.response.send_message(
            embed=discord.Embed(title='',
                                description="This command is not available in this server.",
                                color=discord.Color.red()),
            ephemeral=True)


# Last Optimized [11-11-2024]
@client.tree.command(name="luck", description="all lucky!")
async def lucky_all(interaction: discord.Interaction):
    """OPTIMIZED METHOD"""

    if interaction.guild.id == MAIN_GUILD or interaction.user.mention in permitted_users:
        await interaction.response.defer()
        await add_bot_usage()
        user = await check_profile(interaction)
        user_luck = await TodayLuck.get_or_none(uid=user)
        if not user_luck:
            await lucky_all_embeds(interaction, user)
        else:
            embed = await today_luck_embed(user_luck)
            await interaction.followup.send(embed=embed)

    else:
        await interaction.response.send_message(
            embed=discord.Embed(title='',
                                description="This command is not available in this server.",
                                color=discord.Color.red()),
            ephemeral=True)


# Last Optimization [19-01-2024]
async def get_avatar(interaction):
    try:
        avatar_url = interaction.user.avatar.url
        return avatar_url
    except Exception:
        default_avatar_url = 'https://cdn.discordapp.com/attachments/1171092440233541632/1176439824622833764/Untitled.png?ex=656edff7&is=655c6af7&hm=3e2cd8767c426187fbfc3171749ccf0158152f94a9b64f5acb3ae0a868a907c5&'
        return default_avatar_url


# Last Optimization [13-03-2024]
async def send_error(file, function_name, error, server='Anonymous'):
    embed = discord.Embed(title=f'{server} Server', description=file, color=discord.Color.red())
    embed.add_field(name=function_name, value=error, inline=False)
    user = await client.fetch_user(568179896459722753)
    await user.send(embed=embed)


@client.event
async def on_error(event, *args, **kwargs):
    error = str(sys.exc_info())
    error = error.replace(',', '\n')
    await send_error(__file__, event, error)


async def add_bot_usage():
    today_usage = await BotUsage.get_or_none(date=datetime.datetime.utcnow())
    today_usage.lucky_bot = today_usage.lucky_bot + 1
    await today_usage.save()


async def check_profile(interaction: discord.Interaction):
    user = await Profile.get_or_none(discord_id=str(interaction.user.mention))
    if not user:
        user = Profile(discord_name=str(interaction.user.name), discord_id=str(interaction.user.mention))
        await user.save()
    return user


client.run(os.getenv("TOKEN"))
