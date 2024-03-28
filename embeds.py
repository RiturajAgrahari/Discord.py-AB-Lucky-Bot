import discord


async def help_embed(name, avatar):
    embed = discord.Embed(
        title='Features that we provide',
        description='',
        color=discord.Color.dark_grey()
    )
    embed.add_field(
        name="1. </luck:1171651940879454240>",
        value="This command will show your lucky container, location and weapon for the day.",
        inline=False
    )
    embed.add_field(
        name="* Reset [00:00:00 UTC+0]",
        value="After reset you will be able to get another drop from the above command",
        inline=False
    )
    embed.add_field(
        name="2. </feedback:1172116518738341908>",
        value="Give your ratings and review through this command, and we will continue to improve the bot!",
        inline=False
    )
    embed.set_author(name=name, icon_url=avatar)
    embed.set_footer(text='Arena Breakout')
    return embed
