import discord
import os

from discord import app_commands
from discord.ext import tasks
from datetime import datetime, timedelta
from typing import Literal
from dotenv import load_dotenv

from embeds import help_embed
from luck import *
from database import check_profile, lucky_claimed, check_status, get_data, reset_data, add_use, add_record,\
    update_dbms, check_event_status, start_trial, test_db
import asyncio
import datetime
from review import review_area
from Plotting import show_graph

load_dotenv()

# MY_GUILD = discord.Object(id=850804938510172182)  # my server

MAIN_GUILD_ID = int(os.getenv("MAIN_SERVER_ID"))
TEST_GUILD_ID = int(os.getenv("TEST_SERVER_ID"))

class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Set up command tree for the first guild
        first_guild = discord.Object(id=MAIN_GUILD_ID)
        self.tree.copy_global_to(guild=first_guild)
        await self.tree.sync(guild=first_guild)

        # Set up command tree for the second guild
        second_guild = discord.Object(id=TEST_GUILD_ID)
        if second_guild.id != MAIN_GUILD_ID:
            self.tree.copy_global_to(guild=second_guild)
            await self.tree.sync(guild=second_guild)


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await check_time.start()
    # global guild_name
    # guild_name = client.guilds[0]  # guild name (Gameozone)
    # print(guild_name)

@tasks.loop(minutes=1)
async def check_time():
    # Get the current UTC time
    current_time_utc = datetime.datetime.utcnow().time()

    # Check if it's UTC 00:00
    if current_time_utc.hour == 0 and current_time_utc.minute == 0:
        await daily_checkup()


@client.event
async def on_message(message):
    if message.channel.type == discord.ChannelType.private:
        print(f'DM --> [{message.author}] : {message.content}')

    else:
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        guild_name = message.guild.name
        # print(f"[{channel}-----{username}------] : {user_message}")

        if message.content == 'test' and message.author.mention == '<@568179896459722753>':
            await send_error(__file__, on_message.__name__, 'error tested successful!', guild_name)

        elif message.content == 'give_error' and message.author.mention == '<@568179896459722753>':
            print(ERROR_TADAA)

        elif message.content == 'check_mysql_status' and message.author.mention == '<@568179896459722753>':
            await test_db()

        elif message.content == 'show_graph' and message.author.mention == '<@568179896459722753>':
            graph = await show_graph()
            await message.channel.send(file=graph)

        elif message.content == 'test_reset_data' and message.author.mention == '<@568179896459722753>':
            await reset_data()
            await send_error(__file__, on_message.__name__, 'Data reset seccessful!', guild_name)

        elif message.content == 'test_add_record' and message.author.mention == '<@568179896459722753>':
            await add_record()
            await send_error(__file__, on_message.__name__, 'Record is updated successfuly!', guild_name)

        elif message.content == 'update_db' and message.author.mention == '<@568179896459722753>':
            await update_dbms()
            await send_error(__file__, on_message.__name__, 'name4 and value4 and summary column added successfully!', guild_name)

        elif message.content == 'hi' and message.author.mention == '<@568179896459722753>':
            print('hi')

    if message.author == client.user:
        pass


# Last Optimization [19-01-2024]
@client.tree.command(name='help', description='Shows help for the bot.')
async def help(interaction: discord.Interaction):
    if interaction.guild.id == MAIN_GUILD_ID:
        avatar = await get_avatar(interaction)
        embed = await help_embed(interaction.user, avatar)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=discord.Embed(title='',
                                                                    description="This command is not available in this server.",
                                                                    color=discord.Color.red()), ephemeral=True)


# Last Optimization [19-01-2024]
@client.tree.command(name="feedback", description="help us to improve")
async def feedback(interaction: discord.Interaction):
    if interaction.guild.id == MAIN_GUILD_ID:
        # channel = client.get_channel(1085405558003204169)
        uid = await check_profile(interaction)
        await review_area(interaction, uid)
    else:
        await interaction.response.send_message(embed=discord.Embed(title='',
                                                                    description="This command is not available in this server.",
                                                                    color=discord.Color.red()), ephemeral=True)


# Not Optimized
@client.tree.command(name="luck", description="all lucky!")
async def lucky_all(interaction: discord.Interaction):
    '''OLD METHOD'''

    if interaction.guild.id == MAIN_GUILD_ID:
        uid = await check_profile(interaction)
        status = await check_status('today_luck', uid)
        avatar = await get_avatar(interaction)
        if status == 'Not Claimed':
                await interaction.response.defer()
                embed, title, description, name1, value1, name2, value2, name3, value3, image, name4, value4, summary = \
                    await lucky_all_embeds(interaction.user, avatar)
                await interaction.followup.send(embed=embed)
                await lucky_claimed('today_luck', uid, title, description, name1, value1, name2, value2, name3, value3, image, name4, value4, summary)
                await add_use(uid)
        else:
            data = await get_data('today_luck', uid)
            await interaction.response.defer()
            embed = await show_embed(data[0], interaction.user, avatar)
            await interaction.followup.send(embed=embed)
    else:
        await interaction.response.send_message(embed=discord.Embed(title='',
                                                                    description="This command is not available in this server.",
                                                                    color=discord.Color.red()), ephemeral=True)

    """NEW METHOD"""

    # await interaction.response.defer()
    # avatar = await get_avatar(interaction)
    # embed, title, description, name1, value1, name2, value2, name3, value3, image = \
    #     await lucky_all_embeds(interaction.user, avatar)
    # response = await start_trial(interaction, value1, value2, value3, image)
    # embed1 = await create_embed(response[0], interaction.user, avatar)
    # await interaction.followup.send(embed=embed1)


# Last Optimization [19-01-2024]
async def get_avatar(interaction):
    try:
        avatar_url = interaction.user.avatar.url
        return avatar_url
    except Exception as e:
        default_avatar_url = 'https://cdn.discordapp.com/attachments/1171092440233541632/1176439824622833764/Untitled.png?ex=656edff7&is=655c6af7&hm=3e2cd8767c426187fbfc3171749ccf0158152f94a9b64f5acb3ae0a868a907c5&'
        return default_avatar_url


# Created at [19-01-2024] --> Need to be Tested
async def daily_checkup():
    try:
        await reset_data()
        await add_record()
        record = await show_graph()
        user = await client.fetch_user(568179896459722753)
        await user.send(file=record)
    except Exception as e:
        pass
        # await send_error(guild_name, __file__, on_ready.__name__, e)


# Last Optimization [19-01-2024] --> Need Relocation
async def send_error(file, function_name, error, server='Anonymous'):
    embed = discord.Embed(title=f'{server} Server',
        description=file,
        color=discord.Color.red()
    )
    embed.add_field(
        name=function_name,
        value=error,
        inline=False
    )
    user = await client.fetch_user(568179896459722753)
    await user.send(embed=embed)


@client.event
async def on_error(event, *args, **kwargs):
    message = args[0] # Gets the message object
    await send_error(__file__, event, 'Their is some error!')


client.run(os.getenv("TOKEN"))
