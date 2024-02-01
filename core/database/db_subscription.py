import asyncpg


class Subscription:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_subscription_table_if_not_exists(self) -> None:
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS subscription (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT,
                job_type TEXT[],
                technologies TEXT[],
                experience TEXT,
                salary_rate TEXT,
                english_lvl TEXT,
                country TEXT[],
                city TEXT[]
            )
        """)

    async def create_subscription(self, telegram_id: int, job_type: list,
                                  technologies: list, experience: str, salary_rate: str,
                                  english_lvl: str, country: list, city: list) -> int:
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

    async def update_subscription(self, subscription_id: int, job_type: list,
                                  technologies: list, experience: str, salary_rate: str,
                                  english_lvl: str, country: list, city: list) -> None:
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
            SELECT id, job_type, technologies, experience, english_lvl, country, city
            FROM subscription
            WHERE id = ANY($1)
        """, subscription_ids)

        result = []
        for subscription in query:
            subscription_dict = dict(subscription)
            result.append(subscription_dict)

        return result

    async def get_subscription_by_id(self, subscription_id: int):
        record = await self.connector.fetchrow("""
            SELECT * 
            FROM subscription
            WHERE id = $1
        """, subscription_id)

        if record:
            return dict(record)
        return None

    async def get_all_subscriptions(self):
        query = await self.connector.fetch("""
            SELECT s.*
            FROM subscription s
            JOIN users u ON s.id = ANY(u.subscriptions)
            WHERE u.sub = TRUE
        """)
        return [dict(record) for record in query]

    # admin statistic
    async def get_statistic_by_category(self, category: str) -> dict:
        query = f"""
            SELECT unnest(string_to_array({category}::text, ',')) as category, COUNT(*) as total_count
            FROM subscription
            GROUP BY category
        """
        rows = await self.connector.fetch(query)

        result = {
            "total": 0,
            "details": {}
        }

        for row in rows:
            category_value = row['category']
            count = row['total_count']
            result["details"][category_value] = count
            result["total"] += count

        return result
