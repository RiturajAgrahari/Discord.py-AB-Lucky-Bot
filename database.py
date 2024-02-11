# Clear bottom test functions!
import discord
import os
import mysql.connector
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()

HOST = os.getenv("MY_SQL_HOST")
USER = os.getenv("MY_SQL_USER")
PASSWORD = os.getenv("MY_SQL_PASSWORD")
DATABASE = os.getenv("MY_SQL_DATABASE")

def open_database():
    mydb = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    return mydb


async def test_db():
    try:
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = 'show databases'
        mycursor.execute(sql)
        data = mycursor.fetchall()
        print(data)
    except Exception as e:
        print(e)
    finally:
        mydb.close()

# Need to add multiple columns and conditions!
async def select_query(column:str, table:str, condition_column:str=None, condition_value:str | int=None,
                       order_by_column:str=None, ascending:bool=True, limit:int=None, offset:int=0):
    sql = f"SELECT {column} FROM {table}"

    if condition_column is None or condition_value is None:
        pass
    else:
        if type(condition_value) is str:
            sql += f" WHERE {condition_column} = '{condition_value}'"
        else:
            sql += f" WHERE {condition_column} = {condition_value}"

    if order_by_column is None:
        pass
    else:
        sql += f" ORDER BY {order_by_column}"

    if not ascending:
        sql += " DESC"

    if limit:
        sql += f" LIMIT {offset}, {limit}"

    mydb = open_database()
    mycursor = mydb.cursor()
    print(f'(sql select query): {sql}')
    mycursor.execute(sql)
    output = mycursor.fetchall()
    mydb.close()
    return output


async def check_profile(interaction):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'select uid from profile where discord_id = "{interaction.user.mention}"'
    mycursor.execute(sql)
    output = mycursor.fetchall()
    mydb.close()
    if len(output) == 0:
        print(f'creating {interaction.user.name} profile...')
        return await creating_main_profile(interaction)
    else:
        return output[0][0]


async def creating_main_profile(interaction):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = "INSERT INTO profile (name, discord_id) VALUES (%s, %s)"
    val = [(interaction.user.name, interaction.user.mention)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()
    uid = await check_profile(interaction)
    # await adding_event_data('today_luck', uid)
    return uid


async def lucky_claimed(event_name, uid, title, description, name1, value1, name2, value2, name3, value3, image, name4, value4, summary):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE {event_name} set status = %s, title = %s, description = %s, name1 = %s, value1 = %s, name2 = %s," \
          f" value2 = %s, name3 = %s, value3 = %s, image = %s, name4 = %s, value4 = %s, summary = %s WHERE uid = {uid}"
    val = [('Claimed', title, description, name1, value1, name2, value2, name3, value3, image, name4, value4, summary)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()


async def check_status(event_name, uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'SELECT status FROM {event_name} WHERE uid = {uid}'
    # sql = f'select check_claim_status({uid}) as claim_status;'
    mycursor.execute(sql)
    data = mycursor.fetchall()
    mydb.close()
    print(data)
    if len(data) == 0:
        await adding_event_data(event_name, uid)
        status = await check_status(event_name, uid)
        return status
    else:
        return data[0][0]


async def check_event_status(uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'SELECT event FROM today_luck WHERE uid = {uid}'
    mycursor.execute(sql)
    data = mycursor.fetchall()
    mydb.close()
    print(data)
    if len(data) == 0:
        await adding_event_data('today_luck', uid)
        status = await check_event_status(uid)
        return status
    else:
        return data[0][0]

async def adding_event_data(event_name, uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'INSERT INTO {event_name} (uid) VALUES (%s)'
    val = [(uid)]
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()


async def get_data(event_name, uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'SELECT title, description, name1, value1, name2, value2, name3, value3, image, name4, value4, summary from {event_name}' \
          f' where uid = {uid}'
    mycursor.execute(sql)
    data = mycursor.fetchall()
    mydb.close()
    print(data)
    return data


async def add_use(uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'UPDATE profile set event_used = event_used + 1, last_used_on = DEFAULT where uid = {uid}'
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


async def add_review(uid, review, star_rating):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'INSERT into bot_review (uid, review, star_rating) VALUES (%s, %s, %s)'
    val = [(uid, review, star_rating)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()


async def reset_data():
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE today_luck SET status = %s, title = %s, description = %s, name1 = %s, value1 = %s, name2 = %s," \
          f" value2 = %s, name3 = %s, value3 = %s, image = %s, name4 = %s, value4 = %s"
    val = [('Not Claimed', '', '', '', '', '', '', '', '', '', '', '')]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()
    print('data reset successful!')


async def check_uses(yesterday_date):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"SELECT count(*) FROM profile WHERE last_used_on ='{yesterday_date}'"
    mycursor.execute(sql)
    data = mycursor.fetchall()[0][0]
    mydb.close()
    return data


async def add_record():
    # today_date = str(date.today()).split('-')
    # yesterday_date = date(int(today_date[0]), int(today_date[1]), int(today_date[2]) - 1)

    today_date = date.today()
    yesterday_date = today_date - timedelta(days=1)
    print(f'Function is running at {today_date} to add record of yesterday: {yesterday_date}')

    uses = await check_uses(str(yesterday_date))
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'INSERT INTO record (date, number_of_uses) VALUES (%s, %s)'
    val = [(str(yesterday_date), uses)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()


async def update_dbms():
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'ALTER TABLE today_luck ADD name4 VARCHAR(100)'
    mycursor.execute(sql)
    data = mycursor.fetchall()
    mydb.close()

    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'ALTER TABLE today_luck ADD value4 VARCHAR(100)'
    mycursor.execute(sql)
    data = mycursor.fetchall()
    mydb.close()

    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'ALTER TABLE today_luck ADD summary VARCHAR(300)'
    mycursor.execute(sql)
    data = mycursor.fetchall()
    mydb.close()


async def start_trial(interaction, val1, val2, val3, img):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"CALL get_data('{interaction.user}', '{interaction.user.mention}', '{val1}', '{val2}', '{val3}', '{img}');"
    mycursor.execute(sql, multi=True)
    response = mycursor.fetchall()
    print(response)
    mydb.close()
    return response