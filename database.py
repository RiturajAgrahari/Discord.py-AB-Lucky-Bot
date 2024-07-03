"""LAST OPTIMIZATION [03-07-2024] """

import os
import mysql.connector
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()

HOST = os.getenv("MY_SQL_HOST")
USER = os.getenv("MY_SQL_USER")
PASSWORD = os.getenv("MY_SQL_PASSWORD")
DATABASE = os.getenv("MY_SQL_DATABASE")


class FetchingDatabaseError(Exception):
    pass


def open_database():
    mydb = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        auth_plugin='mysql_native_password'
    )
    return mydb


async def count_rows(table: str, row: str):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"SELECT COUNT({row}) FROM {table}"
    mycursor.execute(sql)
    output = mycursor.fetchall()[0][0]
    mydb.close()
    return output


async def set_bot_uses_date():
    today_date = date.today()

    updated_date = await select_query("date", table="bot_info", condition_column="date", condition_value=str(today_date))
    if updated_date:
        return "date already updated!"
    else:
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = 'INSERT INTO bot_info (date) VALUES (%s)'
        val = [(str(today_date))]
        mycursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return "New Date row initiated successfully!"


async def reset_data():
    data = await select_query(column="*", table="today_luck")
    if data:
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = f"DELETE FROM today_luck"
        mycursor.execute(sql)
        mydb.commit()
        mydb.close()
        return "Data Reset successfully"
    else:
        return "Data is already erased!"


async def add_record():
    today_date = date.today()
    yesterday_date = today_date - timedelta(days=1)
    last_record_date = await select_query(column="date", table="record", condition_column="date", condition_value=str(yesterday_date))
    if last_record_date:
        return "Record is already updated!"

    else:
        uses = await count_rows("today_luck", "uid")
        mydb = open_database()
        mycursor = mydb.cursor()
        sql = 'INSERT INTO record (date, number_of_uses) VALUES (%s, %s)'
        val = [(str(yesterday_date), uses)]
        mycursor.executemany(sql, val)
        mydb.commit()
        mydb.close()
        return "Record added successfully"


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


# Need to add multiple conditions!
async def update_query(table:str, key_value:dict, condition_column:str=None, condition_value:str | int=None, operation:str='equal'):
    if condition_column is None or condition_value is None:
        condition = ""
    else:
        if type(condition_value) is str or type(condition_value) is None:
            condition = f" WHERE {condition_column} = '{condition_value}'"
        else:
            condition = f" WHERE {condition_column} = {condition_value}"

    set = ""

    for key, value in key_value.items():
        if value == "DEFAULT":
            set += f", {key} = {value}"

        elif type(value) is str:
            set += f", {key} = '{value}'"

        elif type(value) is int:
            if operation == 'equal':
                set += f", {key} = {value}"
            elif operation == 'addition':
                set += f", {key} = {key} + {value}"
            elif operation == 'subtraction':
                set += f", {key} = {key} - {value}"
            else:
                print('wrong operation!')
        else:
            print('wrong value datatype')

    set = set.lstrip(',')

    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f"UPDATE {table} SET{set}{condition}"
    # print(f"(sql update query): {sql}")
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()


async def add_bot_use(today_date):
    await update_query(table="bot_info", key_value={"lucky_bot": 1}, condition_column="date", condition_value=str(today_date), operation="addition")


async def check_profile(interaction):
    output = await select_query(column="uid", table="profile", condition_column="discord_id", condition_value=interaction.user.mention)

    if len(output) == 0:
        print(f'creating {interaction.user.name} profile...')
        return await creating_main_profile(interaction)
    else:
        return output[0][0]


async def get_data(uid):
    data = await select_query(column="location, container, weapon, item, summary", table="today_luck", condition_column="uid", condition_value=uid)
    return data


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


async def add_use(uid):
    await update_query(table="profile", key_value={"event_used": 1, "last_used_on": "DEFAULT"}, condition_column="uid", condition_value=uid, operation="addition")


async def add_review(uid, review, star_rating):
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = f'INSERT into bot_review (uid, review, star_rating) VALUES (%s, %s, %s)'
    val = [(uid, review, star_rating)]
    mycursor.executemany(sql, val)
    mydb.commit()
    mydb.close()


async def update_dbms():
    mydb = open_database()
    mycursor = mydb.cursor()
    sql = 'ALTER TABLE today_luck DROP COLUMN status'
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()



