import asyncpg

from core.settings import settings


async def check_database_exists() -> bool:
    connection = await asyncpg.connect(
        host=settings.db.db_host,
        port=settings.db.db_port,
        user=settings.db.db_user,
        password=settings.db.db_password
    )
    result = await connection.fetchval(f"""
    SELECT COUNT(*) 
    FROM pg_catalog.pg_database 
    WHERE datname = '{settings.db.db_database}'
    """
                                       )
    await connection.close()
    return result == 1


async def create_database() -> None:
    connection = await asyncpg.connect(
        host=settings.db.db_host,
        port=settings.db.db_port,
        user=settings.db.db_user,
        password=settings.db.db_password
    )
    await connection.execute(f"""
    CREATE DATABASE {settings.db.db_database} 
    WITH OWNER = {settings.db.db_user} 
    ENCODING = 'UTF8' 
    CONNECTION LIMIT = -1
    """
                             )
    await connection.close()
