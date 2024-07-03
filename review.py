# Same as server!
# Remove the channel argument from feedback function in main.py

import discord
from discord import ui
from discord.ui import View, Button
from database import add_review


async def review_area(interaction, uid, client):
    class MyModal(discord.ui.Modal, title='Review'):
        review = ui.TextInput(label='Review', placeholder="Enter your review here...", style=discord.TextStyle.long)

        async def on_submit(self, interaction: discord.Interaction):
            await rating_area(interaction, str(self.review), uid, client)

        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

    await interaction.response.send_modal(MyModal())


async def rating_area(interaction1, review, uid, client):
    embed = discord.Embed(title='Rate us!', description='You are just one last step away to complete your feedback!', color=discord.Color.gold())

    class MyView(View):
        def __init__(self):
            super().__init__(timeout=30)
            self.response = None
            self.click_count = 0

        @discord.ui.button(label='1⭐', style=discord.ButtonStyle.red)
        async def one_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 1)
            await send_review(client, review, 1, interaction)

        @discord.ui.button(label='2⭐', style=discord.ButtonStyle.red)
        async def two_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 2)
            await send_review(client, review, 2, interaction)

        @discord.ui.button(label='3⭐', style=discord.ButtonStyle.blurple)
        async def three_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 3)
            await send_review(client, review, 3, interaction)

        @discord.ui.button(label='4⭐', style=discord.ButtonStyle.green)
        async def four_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 4)
            await send_review(client, review, 4, interaction)

        @discord.ui.button(label='5⭐', style=discord.ButtonStyle.green)
        async def five_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 5)
            await send_review(client, review, 5, interaction)

    view = MyView()
    view.response = await interaction1.response.send_message(embed=embed, view=view, ephemeral=True)


async def send_review(client, review, rating, interaction):
    embed = discord.Embed(title="FEEDBACK", description="", color=discord.Color.gold())
    embed.add_field(name="Review", value=review, inline=False)
    embed.add_field(name="Rating", value=f"{rating} ⭐", inline=False)
    embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
    embed.set_footer(text=f"Review added through Lucky Bot")
    user = await client.fetch_user(568179896459722753)
    await user.send(embed=embed)


