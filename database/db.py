import aiosqlite
import os

DB_PATH = "my_bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                joined_at TEXT
            )
        """)

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
        await db.commit()

async def mod_log(user_name, user_id, moderator_name, moderator_id, reason, timestamp):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO mod_log (user_name, user_id, moderator_name, moderator_id, reason, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_name, user_id, moderator_name, moderator_id, reason, timestamp))
        await db.commit()

async def add_user(user_id: int, username: str, joined_at: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT OR REPLACE INTO users (user_id, username, joined_at)
            VALUES (?, ?, ?)
        """, (user_id, username, joined_at))
        await db.commit()