import asyncpg


class Admins:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_admins_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS admins (
            
                password TEXT,
                
                channel_id BIGINT
            )
        """)
        await self.connector.execute("""
        INSERT INTO admins (password) 
        VALUES ($1);
        """, '123')

    async def get_password(self):
        return await self.connector.fetchval("""
        SELECT password FROM admins LIMIT 1;
        """)

    async def set_password(self, new_password: str):
        await self.connector.execute("""
        UPDATE admins SET password = $1;
        """, new_password)