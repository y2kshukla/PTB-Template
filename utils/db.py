import aiomysql
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import asyncio

load_dotenv()

host = os.getenv('HOST');
port = os.getenv('PORT');
database = os.getenv('DATABASE');
user = os.getenv('USER');
password = os.getenv('PASSWORD');

def sync_create_connection():
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,       # e.g., 'localhost' or an IP address
            database=database, # Your database name
            user=user,    # Your username
            password=password # Your password
        )

        if connection.is_connected():
            print('Connected to the database')
            return connection

    except Error as e:
        print(f"Error: {e}")
        return None

async def create_connection():
    try:
        connection = await aiomysql.connect(
            host=host,
            port=port,
            db=database,
            user=user,
            password=password,
            autocommit=True
        )
        print('Connected to the database')
        return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

async def extract_telegram_id(s: str) -> str:
    telegram_id = ''
    for char in s:
        if char.isdigit():
            telegram_id += char
        else:
            break
    return telegram_id
