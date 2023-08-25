import asyncpg


class Sources:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_sources_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                
                id SERIAL PRIMARY KEY,
                link TEXT
            )
        """)
