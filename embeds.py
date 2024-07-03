import discord


# Last Optimization [03-07-2024]
async def help_embed(name, avatar):
    embed = discord.Embed(
        title='Features that we provide',
        description='',
        color=discord.Color.dark_grey()
    )
    embed.add_field(
        name="1. </luck:1171651940879454240>",
        value="Get your daily dose of fortune! This command reveals your lucky **loot, container, location, and weapon*"
              "* for the day. Maximize your chances of success with this insider tip! (Resets daily at 00:00:00 UTC+0)",
        inline=False
    )
    embed.add_field(
        name="2. </feedback:1172116518738341908>",
        value="Help us improve! Share your feedback and reviews directly through this command. Your input is valuable"
              " to us.",
        inline=False
    )
    embed.set_author(name=name, icon_url=avatar)
    embed.set_footer(text='Arena Breakout')
    return embed
