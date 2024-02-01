import asyncpg


class Admins:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_admins_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                password TEXT,
                channel_id BIGINT,
                technologies TEXT[],
                block BOOL DEFAULT FALSE,
                
                last_id INTEGER
            )
        """)

        existing_password = await self.connector.fetchval("""
            SELECT password 
            FROM admins
            LIMIT 1;
        """)

        if existing_password is None:
            await self.connector.execute("""
                INSERT INTO admins (password) 
                VALUES ($1);
            """, '123')

    # password
    async def get_password(self):
        return await self.connector.fetchval("""
            SELECT password 
            FROM admins;
        """)

    async def set_password(self, new_password: str):
        await self.connector.execute("""
            UPDATE admins 
            SET password = $1;
        """, new_password)

    # last_date
    async def get_last_id(self) -> int:
        return await self.connector.fetchval(f"""
            SELECT last_id
            FROM admins 
        """)

    async def update_last_id(self, value: str) -> None:
        await self.connector.execute(f"""
            UPDATE admins 
            SET last_id = $1 
        """, value)

    # hold
    async def get_technologies(self) -> list:
        result = await self.connector.fetchval("""
            SELECT technologies 
            FROM admins
        """)

        return result if result is not None else []

    async def add_technologies(self, technology: str) -> None:
        await self.connector.execute("""
            UPDATE admins
            SET technologies = array_append(technologies, $1)
        """, technology)

    async def remove_technologies(self, technology: str) -> None:
        await self.connector.execute("""
            UPDATE admins
            SET technologies = array_remove(technologies, $1)
        """, technology)

    async def remove_all_technologies(self):
        await self.connector.execute("""
            UPDATE admins
            SET technologies = ARRAY[]::TEXT[], block = FALSE
        """)

    async def block_all_technologies(self):
        await self.connector.execute("""
            UPDATE admins
            SET block = TRUE
        """)

    async def check_block(self):
        return await self.connector.fetchval("""
            SELECT block 
            FROM admins;
        """)
