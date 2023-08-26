import asyncpg


class Subscription:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_subscription_table_if_not_exists(self) -> None:
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS subscription (
            
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT,
                
                job_type TEXT,
                technologies TEXT,
                experience TEXT,
                salary_rate TEXT,
                english_lvl TEXT,
                
                country TEXT,
                city TEXT
            )
        """)

    async def create_subscription(self, telegram_id: int, job_type: str, technologies: list,
                                  experience: str, salary_rate: str, english_lvl: str, country: str, city: str) -> int:
        query = await self.connector.fetchrow("""
            INSERT INTO subscription (telegram_id, job_type, technologies, 
                experience, salary_rate, english_lvl, country, city)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """, telegram_id, job_type, technologies, experience, salary_rate, english_lvl, country, city)

        return query[0]

    async def delete_subscription(self, subscription_id: int) -> int:
        query = await self.connector.fetchval("""
            DELETE FROM subscription
            WHERE id = $1
            RETURNING id
        """, subscription_id)

        return query

    async def update_subscription(self, subscription_id: int, job_type: str, technologies: str,
                                  experience: str, salary_rate: str, english_lvl: str, country: str, city: str) -> None:
        await self.connector.execute("""
            UPDATE subscription
            SET job_type = $2,
                technologies = $3,
                experience = $4,
                salary_rate = $5,
                english_lvl = $6,
                country = $7,
                city = $8
            WHERE id = $1
        """, subscription_id, job_type, technologies, experience, salary_rate, english_lvl, country, city)

    async def get_subscription(self, subscription_ids: list) -> list:
        query = await self.connector.fetch("""
            SELECT id, job_type, technologies, experience, salary_rate, english_lvl, country, city
            FROM subscription
            WHERE id = ANY($1)
        """, subscription_ids)

        result = []
        for subscription in query:
            subscription_dict = dict(subscription)
            result.append(subscription_dict)

        return result
