import asyncpg


class Employee:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    # smm
    async def create_smm_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS smm (
            
                smm_id BIGINT,
                smm_username TEXT
            )
        """)

    async def add_smm(self, smm_id: int, smm_username: str):
        existing_smm = await self.connector.fetchrow("""
            SELECT * 
            FROM smm 
            WHERE smm_id = $1
        """, smm_id)
        if existing_smm:
            raise ValueError("SMM с таким ID уже существует")

        await self.connector.execute("""
            INSERT INTO smm (smm_id, smm_username) 
            VALUES ($1, $2)
        """, smm_id, smm_username)

    async def delete_smm(self, smm_id: int):
        await self.connector.execute("""
            DELETE FROM smm 
            WHERE smm_id = $1
        """, smm_id)

    async def get_smm(self):
        smm_list = await self.connector.fetch("""
            SELECT smm_id, smm_username 
            FROM smm
        """)
        return [smm["smm_username"] for smm in smm_list] or None, \
               [smm["smm_id"] for smm in smm_list] or None

    async def is_user_smm(self, user_id):
        result = await self.connector.fetchval("""
            SELECT COUNT(*) 
            FROM smm 
            WHERE smm_id = $1
        """, user_id)
        return result > 0

    # manager
    async def create_manager_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS manager (
                manager_username TEXT PRIMARY KEY
            )
        """)

    async def add_manager(self, admin_username: str):
        try:
            await self.connector.execute("""
                INSERT INTO manager (manager_username) 
                VALUES ($1)
            """, admin_username)
        except asyncpg.exceptions.UniqueViolationError:
            await self.connector.execute("""
                UPDATE manager 
                SET manager_username = $1
            """, admin_username)

    async def get_manager(self):
        manager = await self.connector.fetchval("""
            SELECT manager_username 
            FROM manager
            """)
        return manager or None
