import os
import sys
import datetime

from log import logger
from db import db_init
from models import BotUsage, Profile

from discord.ext import tasks
from dotenv import load_dotenv
from discord import app_commands
from discord.errors import Forbidden

from luck import *
from embeds import help_embed
from review import review_area
from database import get_data, select_query
from manage import daily_checkup, manage_bot


# LOADING ENV
load_dotenv()


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
    await check_time.start()


# Last Optimization [03-07-2024]
@tasks.loop(minutes=1)
async def check_time():
    # Get the current UTC time
    try:
        current_time_utc = datetime.datetime.utcnow().today()
    except Exception:
        current_time_utc = datetime.datetime.now(datetime.datetime.UTC)

    # Check if it's UTC 00:00
    if current_time_utc.hour == 0 and current_time_utc.minute == 0:
        response = await daily_checkup(client)
        print(response)


# Last Optimization [03-07-2024]
@client.event
async def on_message(message):
    # Check if the message author is not client itself
    if message.author == client.user:
        pass

    elif message.channel.type == discord.ChannelType.private:
        print(f'DM --> [{message.author}] : {message.content}')
        if message.content == "**reset" and message.author.mention == '<@568179896459722753>':
            await manage_bot(client)

    # Message in server channels
    else:
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        guild_name = message.guild.name
        # print(f"[{channel}-----{username}------] : {user_message}")

        # if message.guild.id == MAIN_GUILD_ID:
        if message.channel.id == 1140635890608255016 or message.channel.id == 1199253624350576692:
            if message.content == "/luck" or "<@1149306688147562578>" in message.content:
                embed = await help_embed(username, message.author.avatar)
                await message.channel.send(embed=embed)

        else:
            if message.content == 'test' and message.author.mention == '<@568179896459722753>':
                await send_error(__file__, on_message.__name__, 'error tested successful!', guild_name)

            elif message.content == 'hi' and message.author.mention == '<@568179896459722753>':
                print('hi')

        # else:
        #     pass


# Last Optimization [03-07-2024]
@client.tree.command(name='help', description='Shows help for the bot.')
async def help_command(interaction: discord.Interaction):
    if interaction.guild.id == MAIN_GUILD or interaction.user.mention == "<@568179896459722753>":
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


# Last Optimization [03-07-2024]
@client.tree.command(name="feedback", description="help us to improve")
async def feedback(interaction: discord.Interaction):
    if interaction.guild.id == MAIN_GUILD or interaction.user.mention == "<@568179896459722753>":
        await add_bot_usage()
        user = await Profile.get_or_none(discord_id=str(interaction.user.mention))
        if not user:
            user = Profile(discord_name=str(interaction.user.name), discord_id=str(interaction.user.mention))
            await user.save()
        await review_area(interaction, user, client)
    else:
        await interaction.response.send_message(
            embed=discord.Embed(title='',
                                description="This command is not available in this server.",
                                color=discord.Color.red()),
            ephemeral=True)


# # Last Optimized [03-07-2024]
# @client.tree.command(name="luck", description="all lucky!")
# async def lucky_all(interaction: discord.Interaction):
#     """OPTIMIZED METHOD"""
#
#     if interaction.guild.id == MAIN_GUILD_ID:
#         await add_bot_use(datetime.date.today())
#         uid = await check_profile(interaction)
#         status = await select_query("*", table="today_luck", condition_column="uid", condition_value=uid)
#         print(status)
#
#         if not status:
#             try:
#                 await interaction.response.defer()
#                 await lucky_all_embeds(interaction.user, interaction, uid)
#             except discord.errors.NotFound as e:
#                 print(e)
#             except Exception as e:
#                 print(e)
#
#         else:
#             try:
#                 await interaction.response.defer()
#                 data = await get_data(uid)
#                 embed = await show_embed(data[0])
#                 await interaction.followup.send(embed=embed)
#             except Exception as e:
#                 print(e)
#
#     else:
#         await interaction.response.send_message(
#             embed=discord.Embed(title='',
#                                 description="This command is not available in this server.",
#                                 color=discord.Color.red()),
#             ephemeral=True)
#

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


client.run(os.getenv("TOKEN"))
