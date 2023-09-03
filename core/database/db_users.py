from datetime import date, timedelta

import asyncpg
import pandas as pd


class Users:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_users_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS users (
                
                telegram_id BIGINT PRIMARY KEY,
                username TEXT,
                email TEXT,
                linked_in TEXT,
                subscriptions BIGINT[], 
                date DATE
            )
        """)

    async def add_user(self, telegram_id, username, email, linked_in):
        user_exists = await self.user_exists(telegram_id)
        if not user_exists:
            current_date = date.today()
            await self.connector.execute("""
                INSERT INTO users (telegram_id, username, email, linked_in, date)
                VALUES ($1, $2, $3, $4, $5)
            """, telegram_id, username, email, linked_in, current_date)

    async def user_exists(self, telegram_id):
        user = await self.connector.fetchrow("""
            SELECT * 
            FROM users
            WHERE telegram_id = $1
        """, telegram_id)
        return user is not None

    async def get_subscriptions(self, telegram_id: int) -> list:
        result = await self.connector.fetchval("""
            SELECT subscriptions 
            FROM users
            WHERE telegram_id = $1
        """, telegram_id)

        return result if result is not None else []

    async def add_subscriptions(self, telegram_id: int, subscription_id: int) -> None:
        await self.connector.execute("""
            UPDATE users
            SET subscriptions = array_append(subscriptions, $2)
            WHERE telegram_id = $1
        """, telegram_id, subscription_id)

    async def remove_subscriptions_by_id(self, telegram_id: int, subscription_id: int) -> None:
        await self.connector.execute("""
            UPDATE users
            SET subscriptions = array_remove(subscriptions, $2)
            WHERE telegram_id = $1
        """, telegram_id, subscription_id)

    # admin
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

    async def export_to_excel(self, table_name: str, filename: str):
        query = f"SELECT * FROM {table_name}"
        records = await self.connector.fetch(query)
        if not records:
            return False
        else:
            df = pd.DataFrame(records, columns=records[0].keys())
            df.to_excel(filename, engine='openpyxl', index=False)
