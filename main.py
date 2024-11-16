import os
import sys
import traceback
import datetime
import functools

import discord

from log import logger
from db import db_init
from models import BotUsage, Profile, TodayLuck

from discord.ext import tasks
from dotenv import load_dotenv
from discord import app_commands
from discord.errors import Forbidden

from luck import lucky_all_embeds
from embeds import help_embed, today_luck_embed, wrong_server_embed
from review import review_area
from config import reset_data

from config import config_bot


# LOADING ENV
load_dotenv()

permitted_users = ['<@568179896459722753>']

DEBUG = bool(int(os.getenv("DEBUG")))


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


# Last Optimization [16-11-2024]
def catch_error_decorator():
    def decorator_for_async_func(func):
        @functools.wraps(func)
        async def catch_error(*args):
            try:
                return await func(*args)
            except Exception:
                try:
                    interaction: discord.Interaction = args[0] if len(args) >= 1 else None
                    await send_error(
                        __file__,
                        func.__name__,
                        str(interaction.guild.name) if isinstance(interaction, discord.Interaction) else None
                    )
                except Exception as e:
                    # Sending an email to me!
                    print(e)

        return catch_error
    return decorator_for_async_func


# Last Optimization [16-11-2024]
@client.event
@catch_error_decorator()
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    await db_init()
    await reset_function.start()


# Last Optimization [16-11-2024]
@tasks.loop(minutes=1)
@catch_error_decorator()
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


# Last Optimization [16-11-2024]
@client.event
async def on_message(message):
    # Check if the message author is not client itself
    if message.author == client.user:
        pass

    # Checks if someone Dmed the Bot
    elif message.channel.type == discord.ChannelType.private:
        print(f'DM --> [{message.author}] : {message.content}')

    # Message in server channels
    else:
        username = str(message.author).split('#')[0]
        user_message = str(message.content)
        channel = str(message.channel.name)
        guild_name = str(message.guild.name)
        if DEBUG is True:
            print(f"[----[{guild_name.center(10)}]--[channel:{channel}]--[user:{username}]----] : {user_message}")

        if message.author.mention in permitted_users:
            if user_message == "tommy!":
                await message.reply(content="wuff wuff!")

            elif user_message == "$config-lucky":
                await config_bot(message, client)


# Last Optimization [16-11-2024]
@client.tree.command(name='help', description='Shows help for the bot.')
@catch_error_decorator()
async def help_command(interaction: discord.Interaction):
    if interaction.guild.id == MAIN_GUILD or interaction.user.mention in permitted_users:
        await add_bot_usage()
        avatar = await get_avatar(interaction)
        embed = await help_embed(interaction.user, avatar)
        await interaction.response.send_message(embed=embed)
    else:
        await interaction.response.send_message(embed=await wrong_server_embed(), ephemeral=True)


# Last Optimized [16-11-2024]
@client.tree.command(name="feedback", description="help us to improve")
@catch_error_decorator()
async def feedback(interaction: discord.Interaction):
    if interaction.guild.id == MAIN_GUILD or interaction.user.mention in permitted_users:
        await add_bot_usage()
        user = await check_profile(interaction)
        await review_area(interaction, user, client)
    else:
        await interaction.response.send_message(embed=await wrong_server_embed(), ephemeral=True)


# Last Optimized [16-11-2024]
@client.tree.command(name="luck", description="all lucky!")
@catch_error_decorator()
async def lucky_all(interaction: discord.Interaction):
    """OPTIMIZED METHOD"""
    if interaction.guild.id == MAIN_GUILD or interaction.user.mention in permitted_users:
        await interaction.response.defer()
        await add_bot_usage()
        user = await check_profile(interaction)
        user_luck = await TodayLuck.get_or_none(uid=user)
        if not user_luck:
            await lucky_all_embeds(interaction, user, DEBUG)
        else:
            embed, view = await today_luck_embed(user_luck, DEBUG)
            await interaction.followup.send(embed=embed, view=view)

    else:
        await interaction.response.send_message(embed=await wrong_server_embed(), ephemeral=True)


# Last Optimized [16-11-2024]
async def get_avatar(interaction):
    try:
        avatar_url = interaction.user.avatar.url
        return avatar_url
    except Exception:
        default_avatar_url = 'https://cdn.discordapp.com/attachments/1171092440233541632/1176439824622833764/Untitled.png?ex=656edff7&is=655c6af7&hm=3e2cd8767c426187fbfc3171749ccf0158152f94a9b64f5acb3ae0a868a907c5&'
        return default_avatar_url


# Last Optimization [16-11-2024]
@catch_error_decorator()
async def send_error(absolute_file_path, function_name, server='Anonymous'):
    relative_file_path = str(absolute_file_path).split("/")[-1: -3: -1]
    relative_file_path.reverse()
    ex_type, ex, tb = sys.exc_info()
    traceback.print_tb(tb)
    ### traceback data storer
    # cf = traceback.format_list(traceback.extract_tb(tb))
    # with open("error.txt", "w") as error_file:
    #     error_file.write(str("".join(cf)))

    embed = discord.Embed(
        title=f'{server if server else "Anonymous"} Server',
        description="🔴 An error occurred! ⚠",
        color=discord.Color.red(),
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(
        name="📎 Path",
        value=f"{'/'.join(relative_file_path)}",
        inline=False
    )
    embed.add_field(
        name="🎛️ Function",
        value=f"{function_name}",
        inline=False
    )
    embed.add_field(
        name="📈 Error",
        value=f"**{ex_type}**\n {ex}",
        inline=False
    )
    embed.set_footer(text='Timezone : UTC 00:00')
    user = await client.fetch_user(568179896459722753)
    await user.send(embed=embed)
    ### NOTE: enable above traceback by uncommenting traceback writer in this function above
    ### before uncommenting the next line
    # await user.send(embed=embed, file=discord.File("error.txt"))


@client.event
@catch_error_decorator()
async def on_error(event, *args, **kwargs):
    await send_error(__file__, event)


@catch_error_decorator()
async def add_bot_usage():
    today_usage = await BotUsage.get_or_none(date=datetime.datetime.today)
    today_usage.lucky_bot = today_usage.lucky_bot + 1
    await today_usage.save()


@catch_error_decorator()
async def check_profile(interaction: discord.Interaction):
    user = await Profile.get_or_none(discord_id=str(interaction.user.mention))
    if not user:
        user = Profile(discord_name=str(interaction.user.name), discord_id=str(interaction.user.mention))
        await user.save()
    return user


def main():
    client.run(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
