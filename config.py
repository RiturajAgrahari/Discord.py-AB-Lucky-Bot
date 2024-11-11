import discord
from discord.ui import View
from Plotting import show_graph
from models import TodayLuck, BotUsage

from log import logger


async def config_bot(message, client):
    logger.info(f"{message.author.mention} is configuring the bot!")
    embed = discord.Embed(
        title="BOT CONFIGURATION!",
        description="configure Lucky Bot functionality here.",
        color=discord.Color.red()
    )
    # embed.add_field(name="_NOTE:_", value="Use the button implement changes after doing any configuration to make sure"
    #                                       " that the update is successfully implemented.", inline=False)

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=60)
            self.delete = True
            self.viewing_user = None

        @discord.ui.button(label='Check Stats', style=discord.ButtonStyle.gray)
        async def check_bot_stats(self, interaction: discord.Interaction, button: discord.ui.Button):
            graph = await show_graph()
            user = await client.fetch_user(interaction.user.id)  # extract my user
            await user.send(file=graph)  # send the graph to me! :)
            await interaction.response.send_message(f"`>>> Record is sent in your DM`", ephemeral=True)
            await interaction.message.delete()

        @discord.ui.button(label='Close config menu', style=discord.ButtonStyle.gray)
        async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.message.delete()

        async def interaction_check(self, interaction: discord.Interaction):
            # Check if the interaction is from the original user
            if interaction.user == self.viewing_user:
                return True
            else:
                await interaction.response.send_message("`>>> Access Denied!`", ephemeral=True)

        async def on_timeout(self) -> None:
            if self.delete:
                await response.delete()

    view = MyView()
    view.viewing_user = message.author
    response = await message.reply(embed=embed, view=view)


# Last Updated [11-11-2024]
async def reset_data(client):
    # Clear the -today_luck- table
    await TodayLuck.all().delete()

    # Initiate a row with new date with 0 value in -bot_info- table
    new_usage = BotUsage(fandom_bot=0)
    await new_usage.save()

    # create a daily graph
    record = await show_graph()
    user = await client.fetch_user(568179896459722753)  # extract my user
    await user.send(file=record)  # send the graph to me! :)