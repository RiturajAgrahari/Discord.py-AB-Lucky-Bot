import bs4
import discord
import requests
from bs4 import BeautifulSoup
import asyncio
import mysql.connector
from discord.ui import View
from database import select_query
# new library added
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def open_database():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",
        database="arena_breakout"
    )
    return mydb


# async def notify_user(client):
#     data = await select_query(column='*', table='notify')
#     print(data)
#     for i in range(0, len(data)):
#         user = data[i]
#         await check_notification(user, client)


async def adding_data():
    mydb = await open_database()
    mycursor = mydb.cursor()
    sql = "INSERT INTO profile (course, job, date, last_date, user, user_id) VALUES (%s, %s, %s, %s, %s, %s)"
    val = [(course, job, date, last_date, user, user_id)]
    mycursor.executemany(sql, val)
    mydb.commit()
    # id = await id_check(discord_id)
    mydb.close()
    a = profile(discord_id, 'discord_id')
    id = a.get_id()
    await creating_game_profile(id, stat)


# async def check_notification(user, client):
#     r = requests.get(url=f'http://rcvaranasi.ignou.ac.in/')
#
#     soup = BeautifulSoup(r.text, 'html.parser')
#     # print(soup.prettify())
#
#     my_divs = soup.find_all('div', class_="ancmnt_txt ancmnt_txtlink")
#     for div in my_divs:
#         # print(div)
#         my_anchor = div.find('a')
#         if my_anchor and user[2] != my_anchor.text:
#             print("Link:", my_anchor.get('href'))
#             print("Text:", my_anchor.text)
#             embed = await send_notification(str(my_anchor.get('href')), str(my_anchor.text), user)
#             user_unique_id = user[1]
#             user = await client.fetch_user(user_unique_id)
#             await user.send(embed=embed)
#             break
#         else:
#             print("Nothing new to notify...")
#             break
#
#     # await add_user_data(courses[j], top.text, time.text, last_date='Not defined', user=data[i][1],
#     #                     user_id=user_id)


async def send_notification(link, content, user):
    print(link)
    print(content)
    print(len(content))
    print(user[1])
    embed = discord.Embed(title='IGNOU Announcement (RC Varanasi)',
                          description=content,
                          color=discord.Color.green())

    # embed.set_thumbnail(url=link)

    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE notify SET content = %s, link = %s WHERE discord_id = '{user[1]}';"
    val = [(content, link)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()

    return embed


# async def send_bank_offers():
#     options = Options()
#     options.add_argument('--headless')
#     options.add_experimental_option("detach", True)
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="120.0.6099.111").install()),
#                               options=options)
#
#     driver.get(
#         url='https://www.amazon.in/Ergonomic-Warranty-Adjustable-Armrests-Mechanism/dp/B0BZPJQ2X2/ref=sr_1_5?crid=1DIKKB45H97EV&keywords=Da%2BURBAN%C2%AE%2BMerlion%2BOffice%2BChair%2CHigh%2BBack%2BMesh%2BErgonomic%2BHome%2BOffice%2BDesk%2BChair%2Bwith%2B3%2BYears%2BWarranty%2C%2BAdjustable%2BArmrests%2CAdjustable%2BLumbar%2BSupport%2CTilt%2BLock%2BMechanism%2B(Grey)&nsdOptOutParam=true&qid=1703172922&sprefix=da%2Burban%2Bmerlion%2Boffice%2Bchair%2Chigh%2Bback%2Bmesh%2Bergonomic%2Bhome%2Boffice%2Bdesk%2Bchair%2Bwith%2B3%2Byears%2Bwarranty%2C%2Badjustable%2Barmrests%2Cadjustable%2Blumbar%2Bsupport%2Ctilt%2Block%2Bmechanism%2Bgrey%2B%2Caps%2C209&sr=8-5&th=1')
#
#     driver.maximize_window()
#
#     driver.execute_script("window.scrollTo(0, 500)")
#
#     element = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'a-size-base a-link-emphasis vsx-offers-count')]")))
#
#     driver.execute_script("arguments[0].click();", element)
#
#     sleeping = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
#                                                                                "//div[@class='a-section vsx-offers-desktop-lv__item']//h1 | //div[@class='a-section vsx-offers-desktop-lv__item']//p")))
#
#     all_offers = driver.find_elements("xpath",
#                                       "//div[@class='a-section vsx-offers-desktop-lv__item']//h1 | //div[@class='a-section vsx-offers-desktop-lv__item']//p")
#
#     get_offers = int(len(all_offers) / 2)
#
#     embed = discord.Embed(title='Bank Offers',
#                           description='current bank offers available for the chair you want!',
#                           color=discord.Color.green())
#
#     for i in range(0, get_offers, 2):
#         embed.add_field(name=all_offers[i].get_attribute("innerHTML"),
#                         value=all_offers[i+1].get_attribute("innerHTML"),
#                         inline=False)
#
#     return embed



