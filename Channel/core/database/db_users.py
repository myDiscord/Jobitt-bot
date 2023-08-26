from datetime import date, timedelta

import asyncpg


class Users:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_users_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS users (
                
                user_id SERIAL PRIMARY KEY,
                
                index INTEGER,
                telegram_id BIGINT,
                username TEXT,
                date DATE
            )
        """)

    async def add_user(self, telegram_id: int, username: str):
        existing_user = await self.connector.fetchrow("""
            SELECT * 
            FROM users 
            WHERE telegram_id = $1
        """, telegram_id)
        if existing_user is None:
            current_date = date.today()
            await self.connector.execute("""
                INSERT INTO users (telegram_id, username, date) 
                VALUES ($1, $2, $3)
            """, telegram_id, username, current_date)

    async def get_users(self):
        result = await self.connector.fetch("""
            SELECT telegram_id 
            FROM users
        """)
        return [row['telegram_id'] for row in result]

    async def get_statistics(self):
        today = date.today()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        year_ago = today - timedelta(days=365)

        total = await self.connector.fetchval("SELECT COUNT(*) FROM users")
        today_count = await self.connector.fetchval(
            "SELECT COUNT(*) FROM users WHERE date = $1", today
        )
        week = await self.connector.fetchval(
            "SELECT COUNT(*) FROM users WHERE date >= $1", week_ago
        )
        month = await self.connector.fetchval(
            "SELECT COUNT(*) FROM users WHERE date >= $1", month_ago
        )
        year = await self.connector.fetchval(
            "SELECT COUNT(*) FROM users WHERE date >= $1", year_ago
        )

        return total, today_count, week, month, year

    async def get_new_users(self, target_date: date) -> int:
        return await self.connector.fetchval("""
            SELECT COUNT(*) FROM users
            WHERE date = $1
        """, target_date)
