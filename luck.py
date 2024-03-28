import discord
import random
import fandom
from database import lucky_claimed, add_use

fandom.set_wiki('arena-breakout')

none = None

# containers = ['Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox', 'Cash Register', 'Drawer',
#               'Gym Bag', 'Suitcase', 'Winter Coat', 'Ordinary Jacket', 'Work Clothes', 'Military Computer',
#               'Home Computer', 'Storage Box', 'Document Box', 'Locker', 'Office Drawer', 'Business Suitcase',
#               'Chemical Warfare Suit']
# popup = [0, 4, 5, 6, 7, 11, 12, 14, 15]
# for c in containers:
#     if containers.index(c) in popup:
#         print(f'\'{c}\',', end=' ')
#         # pass
#     else:
#         pass
#         # print(f'\'{c}\',', end=' ')

NEW = {'': {
           'Farm': {
               'high value area': {
                   'Motel': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox', 'Cash Register', 'Drawer', 'Gym Bag',
                       'Suitcase', 'Winter Coat', 'Ordinary Jacket', 'Work Clothes', 'Military Computer'
                   ],
                   'Stables': [
                       'Safe', 'Pro Toolbox', 'Gym Bag', 'Ordinary Jacket', 'Document Box'
                   ],
                   'Loading Area': ['Ordinary Jacket']
               },
               'medium value area': {
                   'Loading Area': ['Ordinary Jacket'],
                   'Villa': [
                       'Safe', 'Gym Bag', 'Winter Coat', 'Ordinary Jacket', 'Work Clothes', 'Home Computer', 'Locker',
                       'Office Drawer'
                   ],
                   'Grain Trade Center': [
                       'Electronic Safe', 'Cash Register', 'Drawer', 'Gym Bag', 'Suitcase', 'Home Computer',
                       'Document Box'
                   ]
               }
           },
           'Valley': {
               'high value area': {
                   'Beach Villa': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Work Clothes', 'Military Computer', 'Home Computer', 'Document Box',
                       'Business Suitcase'
                   ]
               },
               'medium value area': {
                   'Small Factory Basement': [
                       'Safe', 'Home Toolbox', 'Pro Toolbox', 'Drawer', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Work Clothes', 'Military Computer', 'Home Computer', 'Document Box',
                       'Locker', 'Chemical Warfare Suit'
                   ],
                   'Port': [
                       'Safe', 'Home Toolbox', 'Pro Toolbox', 'Drawer', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Storage Box', 'Document Box', 'Business Suitcase'
                   ]
               }
           },
           'Northridge': {
               'high value area': {
                   'Northridge Hotel': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox', 'Drawer', 'Gym Bag', 'Suitcase',
                       'Winter Coat', 'Ordinary Jacket', 'Work Clothes', 'Military Computer', 'Home Computer'
                   ]
               },
               'medium value area': {
                   'Cable Car Station': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox'
                   ],
                   'Camp Services': [
                       'Safe', 'Home Toolbox', 'Pro Toolbox', 'Drawer', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Military Computer', 'Home Computer', 'Storage Box'
                   ],
                   'Sewage Plant': [
                       'Home Toolbox', 'Gym Bag', 'Ordinary Jacket'
                   ]
               }
           },
           'Armory': {
               'high value area': {
                   'Armory': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Military Computer', 'Home Computer', 'Document Box', 'Office Drawer',
                       'Business Suitcase'
                   ]
               },
               'medium value area': {
                   'Gas Station': [
                       'Safe', 'Home Toolbox', 'Pro Toolbox', 'Cash Register', 'Drawer', 'Gym Bag', 'Suitcase',
                       'Work Clothes', 'Document Box', 'Office Drawer', 'Business Suitcase'
                   ],
                   'Barn': ['Winter Coat', 'Locker', 'Office Drawer', 'Business Suitcase']
               }
           }
},
       "Lockdown": {
           'Farm': {
               'high value area': {
                   'Motel': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Cash Register', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Work Clothes', 'Military Computer', 'Document Box', 'Locker',
                       'Office Drawer', 'Business Suitcase'
                   ]
               },
               'medium value area': {
                   'Loading Area': [
                       'Ordinary Jacket', 'Locker'
                   ],
                   'Villa': [
                       'Safe', 'Gym Bag', 'Ordinary Jacket', 'Work Clothes', 'Military Computer', 'Home Computer',
                       'Document Box', 'Locker', 'Office Drawer'
                   ],
                   'Grain Trade Center': [
                       'Electronic Safe', 'Cash Register', 'Drawer', 'Gym Bag', 'Suitcase', 'Military Computer',
                       'Home Computer', 'Document Box', 'Locker'
                   ]
               }
           },
           'Valley': {
               'high value area': {
                   'Beach Villa': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Work Clothes', 'Military Computer', 'Home Computer', 'Storage Box',
                       'Document Box', 'Office Drawer', 'Business Suitcase'
                   ]
               },
               'medium value area': {
                   'Small Factory Basement': [
                       'Safe', 'Home Toolbox', 'Pro Toolbox', 'Drawer', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Work Clothes', 'Military Computer', 'Home Computer', 'Document Box',
                       'Locker', 'Chemical Warfare Suit'
                   ],
                   'RV Camp': [
                       'Safe', 'Home Toolbox', 'Suitcase', 'Winter Coat', 'Ordinary Jacket', 'Storage Box'
                   ],
                   'Port': [
                       'Safe', 'Home Toolbox', 'Pro Toolbox', 'Drawer', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Storage Box', 'Document Box', 'Business Suitcase'
                   ]
               }
           },
           'Northridge': {
               'high value area': {
                   'Northridge Hotel': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox', 'Gym Bag', 'Suitcase', 'Winter Coat',
                       'Ordinary Jacket', 'Work Clothes', 'Military Computer', 'Home Computer', 'Document Box',
                       'Locker', 'Office Drawer', 'Business Suitcase'
                   ]
               },
               'medium value area': {
                   'Cable Car Station': [
                       'Electronic Safe', 'Safe', 'Home Toolbox', 'Pro Toolbox', 'Drawer', 'Gym Bag', 'Winter Coat',
                       'Ordinary Jacket', 'Military Computer', 'Home Computer', 'Storage Box', 'Document Box', 'Locker',
                       'Office Drawer', 'Business Suitcase'
                   ],
                   'Camp Services': [
                       'Safe', 'Home Toolbox', 'Pro Toolbox', 'Locker'
                   ],
                   'Sewage Plant': [
                       'Home Toolbox', 'Ordinary Jacket', 'Business Suitcase'
                   ]
               }
           },
}
       }


Weapons = {
    'Assault Rifles': {'M4A1': none, 'H416': none, 'AKM': none, 'AK-74N': none, 'AK102': none, 'AKS74U': none,
                       'FAL': none, 'F2000': none, 'AR57': none, 'MOR': none},
    'Submachine Guns': {'MPX': none, 'MP5': none, 'MP40': none, 'MP45': none, 'UZI': none, 'P90': none, 'M3A1': none,
                        'MAC10': none, 'QC61': none, 'UMP45': none, 'Vector9': none, 'Vector45': none, 'T79': none,
                        'T85': none},
    'Marksman Rifles': {'VSS': none, 'SVDS': none, 'M110': none, 'MK14': none},
    'Bolt-Action Rifles': {'Mosin': none, 'AX50': none, 'AR30': none, 'SJ16': none},
    'Machine Gun': {'RPK16': none},
    'Shotguns': {'S12K': none, 'USAS12': none, 'MP133': none, 'M870': none},
    'Carbines': {'SKS': none, 'SA85M': none, 'MINI14': none, 'M96': none, 'M14': none, 'BM59': none},
    'Pistols': {'G18C': none, 'G17': none, 'Deagle': none, 'Gold Deagle': none, 'M9A3': none, 'CZ52': none,
                'M1911': none, 'M45A1': none, 'T54': none, 'T05': none, 'MP9': none}
}

High_Value_Loot = {
    "Gold Cheetah": none,
    "Com. Coin": none,
    "Vase": none,
    "Gold Watch": none,
    "Gold Lion": none,
    "Clock": none,
    "Teapot": none,
    "Silver Badge": none,
    "Silver Chain": none,
    "Gold Bracelet": none,
    "Porcelain": none,
    "Gold-rimmed": none,
    "Album": none,
    "Player": none,
    "Watch": none,
    "Stamp": none,
    "Spur": none,
    "Chain": none,
    "Gold": none,
    "Ring": none,
    "Brooch": none,
    "Document": none,
    "Gold Cube": none,
    "Gold Necklace": none,
    "Gold Cup": none,
    "Typewriter": none,
    "Cane": none,
}

Summaries = [
    "In the Dark Zone, a stockpile of weapons and equipment will always come in handy.",
    "Storing up valuable junk and waiting for the right time to use it is a good strategy.",
    "Ammo is the most reliable resource in the Dark Zone."
    "More equipment means more opportunities. You can't go wrong with this strategy.",
    "Stored Koen can be used to buy important supplies.",
    "Food and drink are always important resources in the Dark Zone.",
    "Collecting rare keys is a big part of surviving in the Dark Zone.",
    "Perhaps the secret is in the next raid!",
    "Accumulating wealth is the key to survival in the DZ.",
    "Bit by bit, your wealth is constantly expanding.",
    "Overnight millionaires are no myth in the Dark Zone.",
    "Defeating the strong is a mark of power in the Dark Zone.",
    "Fortune really does favor the bold."
]

hvl = {}


async def show_embed(data, name, avatar):
    embed = discord.Embed(
        title="Today's Lucky Loot:", description=data[3], color=discord.Color.red()
    )
    embed.add_field(name='Lucky Location', value=data[0], inline=False)
    embed.add_field(name='Lucky Container', value=data[1], inline=True)
    embed.add_field(name='Lucky Gun', value=data[2], inline=True)
    embed.set_footer(text=data[4])

    for values in Weapons.values():
        if data[2] in values:
            if values[data[2]]:
                image = values[data[2]]
            else:
                search = fandom.search(str(data[2]).capitalize(), results=1)
                page = fandom.page(title=search[0][0], pageid=search[0][1])
                image = page.images[0]
                values[data[2]] = image

    embed.set_image(url=image)

    if High_Value_Loot[data[3]]:
        image2 = High_Value_Loot[data[3]]
    else:
        search2 = fandom.search(str(data[3]).capitalize(), results=1)
        page2 = fandom.page(title=search2[0][0], pageid=search2[0][1])
        image2 = page2.images[0]
        High_Value_Loot[data[3]] = image2

    embed.set_thumbnail(url=image2)
    return embed


async def lucky_all_embeds(name, avatar, interaction, uid):
    random_mode = list(NEW.keys())[random.randint(0, len(NEW)-1)]
    maps = NEW[random_mode]
    random_map = list(maps.keys())[random.randint(0, len(maps)-1)]
    area = maps[random_map]
    random_area = list(area.keys())[random.randint(0, len(area)-1)]
    location = area[random_area]
    random_location = list(location.keys())[random.randint(0, len(location)-1)]
    container = location[random_location]
    random_container = container[random.randint(0, len(container)-1)]
    random_category = list(Weapons.keys())[random.randint(0, len(Weapons)-1)]
    weapons = Weapons[random_category]
    random_weapon = list(weapons.keys())[random.randint(0, len(weapons)-1)]
    random_loot = list(High_Value_Loot.keys())[random.randint(0, len(High_Value_Loot)-1)]
    random_summary = Summaries[random.randint(0, len(Summaries)-1)]
    centered_name = str(name).center(30, '-')
    data = {'location': random_location, 'container': random_container, 'weapon': random_weapon,
            'category': random_category, 'loot': random_loot}
    print(f'[{centered_name}] : {data}\n')

    embed = discord.Embed(
        title="Today's Lucky Loot:",
        description=random_loot,
        color=discord.Color.green()
    )
    embed.add_field(
        name=f'Lucky Location',
        value=f'{random_location} ({random_map} {random_mode})',
        inline=False
    )
    embed.add_field(
        name=f'Lucky container',
        value=f'{random_container}',
        inline=True
    )
    embed.add_field(
        name='Lucky gun',
        value=f'{random_weapon}',
        inline=True
    )
    # embed.set_author(name=name, icon_url=avatar)
    embed.set_footer(text=random_summary)

    if weapons[random_weapon]:
        image = weapons[random_weapon]
    else:
        search = fandom.search(str(random_weapon).capitalize(), results=1)
        page = fandom.page(title=search[0][0], pageid=search[0][1])
        image = page.images[0]
        weapons[random_weapon] = image

    if High_Value_Loot[random_loot]:
        image2 = High_Value_Loot[random_loot]
    else:
        search2 = fandom.search(str(random_loot).capitalize(), results=1)
        page2 = fandom.page(title=search2[0][0], pageid=search2[0][1])
        image2 = page2.images[0]
        High_Value_Loot[random_loot] = image2

    try:
        embed.set_image(url=f'{image}')
        embed.set_thumbnail(url=f'{image2}')
    except:
        pass

    await interaction.followup.send(embed=embed)
    await lucky_claimed(uid, f'{random_location} ({random_map} {random_mode})', random_container,
                        random_weapon, random_loot, random_summary)
    await add_use(uid)

