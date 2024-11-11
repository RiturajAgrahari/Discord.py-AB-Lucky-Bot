from Plotting import show_graph
from discord.ui import View
import discord

from models import TodayLuck, BotUsage


# Last Updated [03-07-2024]
async def daily_checkup(client):
    # Clear the -today_luck- table
    await TodayLuck.all().delete()

    # Initiate a row with new date with 0 value in -bot_info- table
    new_usage = BotUsage(fandom_bot=0)
    await new_usage.save()

    # create a daily graph
    # record = await show_graph()
    # user = await client.fetch_user(568179896459722753)  # extract my user
    # await user.send(file=record)  # send the graph to me! :)


# Created [03-07-2024]
async def manage_bot(client):
    embed = discord.Embed(title="Manage Lucky Bot", description="", color=discord.Color.gold())
    embed.add_field(name="Daily Reset", value="Complete reset process!", inline=False)
    embed.add_field(name="Send Graph", value="To check the graph!", inline=False)
    embed.add_field(name="Add Record", value="to add daily usage record!", inline=False)
    embed.add_field(name="Add Date", value="to initiate date to store usage!", inline=False)
    embed.add_field(name="Reset Data", value="To only reset the today luck data!", inline=False)
    embed.set_footer(text="add-record > reset data > add date > show graph > sent!")

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=60)

        @discord.ui.button(label="Daily Reset", style=discord.ButtonStyle.red, custom_id="daily_reset")
        async def reset(self, interaction:discord.Interaction, button:discord.ui.Button):
            response = await daily_checkup(client)
            await message.delete()
            await interaction.response.send_message(response, ephemeral=True)

        @discord.ui.button(label="Send Graph", style=discord.ButtonStyle.green, custom_id="send_graph")
        async def send_graph(self, interaction:discord.Interaction, button:discord.ui.Button):
            record = await show_graph()
            await message.delete()
            await interaction.response.send_message(file=record, ephemeral=True)

        @discord.ui.button(label="Add Record", style=discord.ButtonStyle.blurple, custom_id="add_record")
        async def add_record(self, interaction:discord.Interaction, button:discord.ui.Button):
            await message.delete()

        @discord.ui.button(label="Add Date", style=discord.ButtonStyle.blurple, custom_id="set_daily_usage")
        async def add_date(self, interaction:discord.Interaction, button:discord.ui.Button):
            await message.delete()

        @discord.ui.button(label="Reset Data", style=discord.ButtonStyle.blurple, custom_id="reset_data")
        async def reset_data(self, interaction:discord.Interaction, button:discord.ui.Button):
            await message.delete()

        @discord.ui.button(label="Alter database", style=discord.ButtonStyle.red, custom_id="alter_db")
        async def alter_dbms(self, interaction:discord.Interaction, button:discord.ui.Button):
            response = (f" > DB query run successfully: \n"
                        f" > `ALTER TABLE bot_review ADD COLUMN review_on DATE DEFAULT (CURRENT_DATE);`\n"
                        f" > **NOTE:** _Do not run this command again to avoid error in DB_")
            await message.delete()
            await interaction.response.send_message(response, ephemeral=False)

        async def on_timeout(self) -> None:
            try:
                await message.delete()
            except Exception as e:
                print(e)

    view = MyView()
    user = await client.fetch_user(568179896459722753)  # extract my user
    message = await user.send(view=view, embed=embed)

