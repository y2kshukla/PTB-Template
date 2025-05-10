import aiomysql
import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error
import asyncio

load_dotenv()

host = os.getenv('HOST')
port = int(os.getenv('PORT'))
database = os.getenv('DATABASE')
user = os.getenv('USER')
password = os.getenv('PASSWORD')

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

async def create_user_table():
    connection = await create_connection()
    if connection:
        try:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        telegram_id BIGINT NOT NULL UNIQUE,
                        username VARCHAR(255),
                        balance DECIMAL(10, 2) DEFAULT 0.00,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        is_banned BOOLEAN DEFAULT FALSE
                    );
                """)
                print("Users table created successfully.")
        except Exception as e:
            print(f"Error creating Users table: {e}")
        finally:
            connection.close()

async def create_transaction_table():
    connection = await create_connection()
    if connection:
        try:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Transactions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        user_id INT NOT NULL,
                        type ENUM('deposit', 'withdrawal', 'win', 'loss', 'bonus') NOT NULL,
                        amount DECIMAL(10, 2) NOT NULL,
                        balance_after DECIMAL(10, 2) NOT NULL,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
                    );
                """)
                print("Transactions table created successfully.")
        except Exception as e:
            print(f"Error creating Transactions table: {e}")
        finally:
            connection.close()

async def add_user(telegram_id: int, username: str = None):
    connection = await create_connection()
    if connection:
        try:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                    INSERT INTO Users (telegram_id, username)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE username = VALUES(username);
                """, (telegram_id, username))
                await connection.commit()
                print(f"User {telegram_id} added or updated successfully.")
        except Exception as e:
            print(f"Error adding user: {e}")
        finally:
            connection.close()

async def check_user_exists(telegram_id: int) -> bool:
    connection = await create_connection()
    if connection:
        try:
            async with connection.cursor() as cursor:
                await cursor.execute("""
                    SELECT 1 FROM Users WHERE telegram_id = %s;
                """, (telegram_id,))
                result = await cursor.fetchone()
                return result is not None
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False
        finally:
            connection.close()
    return False

async def extract_telegram_id(s: str) -> str:
    telegram_id = ''
    for char in s:
        if char.isdigit():
            telegram_id += char
        else:
            break
    return telegram_id

async def setup_database():
    try:
        await create_user_table()
        await create_transaction_table()
        print("All tables created successfully.")
    except Exception as e:
        print(f"Error setting up database: {e}")

if __name__ == "__main__":
    asyncio.run(setup_database())