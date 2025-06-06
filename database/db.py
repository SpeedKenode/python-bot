import aiosqlite
import os
from datetime import datetime

DB_PATH = "my_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        #mod-log TABLE
        await db.execute("""
            CREATE TABLE IF NOT EXISTS mod_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                user_id INTEGER,
                moderator_name TEXT,
                moderator_id INTEGER,
                reason TEXT,
                timestamp TEXT
            )
        """)

        #warn-case TABLE
        await db.execute("""
            CREATE TABLE IF NOT EXISTS warn_case (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT,
                user_id INTEGER,
                moderator_name TEXT,
                moderator_id INTEGER,
                reason TEXT,
                timestamp TEXT
            )
        """)

        #channel setup TABLE
        await db.execute("""
            CREATE TABLE IF NOT EXISTS setup_channel (
                modlog_channel INT,
                welcome_channel INT,
                goodbye_channel INT
            )
        """)

        #mute TABLE
        await db.execute("""
            CREATE TABLE IF NOT EXISTS mutes (
                user_id INTEGER,
                unmute_time TEXT
            )
        """)

        await db.commit()

async def mod_log(user_name, user_id, moderator_name, moderator_id, reason, timestamp):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO mod_log (user_name, user_id, moderator_name, moderator_id, reason, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_name, user_id, moderator_name, moderator_id, reason, timestamp))
        await db.commit()

async def warn_case(user_name, user_id, moderator_name, moderator_id, reason, timestamp):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO warn_case (user_name, user_id, moderator_name, moderator_id, reason, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_name, user_id, moderator_name, moderator_id, reason, timestamp))
        await db.commit()

async def set_modlog_channel(channel_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO setup_channel (modlog_channel)
            VALUES (?)
        """, (channel_id,))
        await db.commit()

async def set_welcome_channel(channel_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO setup_channel (welcome_channel)
            VALUES (?)
        """, (channel_id,))
        await db.commit()

async def set_goodbye_channel(channel_id):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO setup_channel (goodbye_channel)
            VALUES (?)
        """, (channel_id,))
        await db.commit()

async def get_modlog():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT modlog_channel FROM setup_channel")
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_welcome():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT welcome_channel FROM setup_channel")
        row = await cursor.fetchone()
        return row[0] if row else None

async def get_goodbye():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT goodbye_channel FROM setup_channel")
        row = await cursor.fetchone()
        return row[0] if row else None

async def add_mute(user_id, unmute_time):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO mutes (user_id, unmute_time) VALUES (?, ?)",
            (user_id, unmute_time),
        )
        await db.commit()

async def get_mute():
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT user_id, unmute_time FROM mutes")
        return await cursor.fetchall()

async def remove_mute(user_id, unmute_time):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM mutes WHERE user_id = ? AND unmute_time = ?",
            (user_id, unmute_time),
        )
        await db.commit()