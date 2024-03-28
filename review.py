# Same as server!
# Remove the channel argument from feedback function in main.py

import discord
from discord import ui
from discord.ui import View, Button
from database import add_review


async def review_area(interaction, uid):
    class MyModal(discord.ui.Modal, title='Review'):
        review = ui.TextInput(label='Review', placeholder="Enter your review here...", style=discord.TextStyle.long)

        async def on_submit(self, interaction: discord.Interaction):
            await rating_area(interaction, str(self.review), uid)

        async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
            await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

    await interaction.response.send_modal(MyModal())


async def rating_area(interaction1, review, uid):
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

        @discord.ui.button(label='2⭐', style=discord.ButtonStyle.red)
        async def two_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 2)

        @discord.ui.button(label='3⭐', style=discord.ButtonStyle.blurple)
        async def three_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 3)

        @discord.ui.button(label='4⭐', style=discord.ButtonStyle.green)
        async def four_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 4)

        @discord.ui.button(label='5⭐', style=discord.ButtonStyle.green)
        async def five_star(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction1.edit_original_response(content='Thanks for the review!', embed=None, view=None)
            await add_review(uid, review, 5)

    view = MyView()
    view.response = await interaction1.response.send_message(embed=embed, view=view, ephemeral=True)


