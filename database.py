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
        database=DATABASE,
        auth_plugin='mysql_native_password'
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
    return uid


async def lucky_claimed(uid, location, container, weapon, item, summary):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"INSERT INTO today_luck VALUES (DEFAULT, %s, %s, %s, %s, %s, %s)"
    val = [(uid, location, container, weapon, item, summary)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()


async def get_data(uid):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'SELECT location, container, weapon, item, summary from today_luck where uid = {uid}'
    mycursor.execute(sql)
    data = mycursor.fetchall()
    mydb.close()
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
    sql = f"DELETE FROM today_luck"
    mycursor.execute(sql)
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


async def set_bot_uses_date():
    today_date = date.today()
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'INSERT INTO bot_info (date) VALUES (%s)'
    val = [(str(today_date))]
    mycursor.execute(sql, val)
    mydb.commit()
    mydb.close()


async def bot_uses(today_date):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE bot_info set lucky_bot = lucky_bot + 1 WHERE date = '{today_date}'"
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


async def update_dbms():
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'ALTER TABLE today_luck DROP COLUMN status'
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()
