import asyncpg


class Users:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_users_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS users (
                
                telegram_id BIGINT PRIMARY KEY,
                username TEXT,
                e-mail TEXT,
                linked_in TEXT,
                
                job_type TEXT,
                technologies TEXT[],
                experience TEXT,
                salary_rate TEXT,
                english_lvl TEXT,
                
                country TEXT,
                city TEXT
            )
        """)

    async def add_user(self, telegram_id, username, email, linked_in):
        user_exists = await self.user_exists(telegram_id)
        if not user_exists:
            await self.connector.execute("""
                INSERT INTO users (telegram_id, username, email, linked_in)
                VALUES ($1, $2, $3, $4)
            """, telegram_id, username, email, linked_in)

    async def user_exists(self, telegram_id):
        user = await self.connector.fetchrow("""
            SELECT * FROM users
            WHERE telegram_id = $1
        """, telegram_id)
        return user is not None
