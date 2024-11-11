import discord
import fandom


# cache for image URLs
cache = {}


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


async def today_luck_embed(user_luck):
    embed = discord.Embed(
        title="Today's Lucky Loot:", description=str(user_luck.item), color=discord.Color.blue()
    )
    embed.add_field(name='Lucky Location', value=str(user_luck.location), inline=False)
    embed.add_field(name='Lucky Container', value=str(user_luck.container), inline=True)
    embed.add_field(name='Lucky Gun', value=str(user_luck.weapon), inline=True)
    embed.set_footer(text=str(user_luck.summary))
    if cache.get(str(user_luck.weapon)) is None:
        search_weapon = fandom.search(str(user_luck.weapon).capitalize(), results=1)
        weapon_page = fandom.page(title=search_weapon[0][0], pageid=search_weapon[0][1])
        weapon_image = weapon_page.images[0]
        embed.set_image(url=weapon_image)
        cache[str(user_luck.weapon)] = weapon_image
    else:
        embed.set_image(url=cache.get(str(user_luck.weapon)))

    if cache.get(str(user_luck.item)) is None:
        search_item = fandom.search(str(user_luck.item).capitalize(), results=1)
        item_page = fandom.page(title=search_item[0][0], pageid=search_item[0][1])
        item_image = item_page.images[0]
        embed.set_thumbnail(url=item_image)
        cache[str(user_luck.item)] = item_image
    else:
        embed.set_thumbnail(url=cache.get(str(user_luck.item)))

    return embed