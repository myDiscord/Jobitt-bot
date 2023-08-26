import asyncpg


class Post:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_post_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS post (
            
                id SERIAL PRIMARY KEY,
                
                text TEXT,
                photo TEXT,
                video TEXT,
                caption TEXT,
                circle TEXT,
                
                date_time TIMESTAMP,
                
                buttons_texts TEXT[],
                buttons_urls TEXT[]
            )
        """)

    async def add_row(self, text, photo, video, caption, circle, date_time, button_text, button_url):
        row = await self.connector.fetchrow("""
            INSERT INTO post (text, photo, video, caption, circle, date_time, buttons_texts, buttons_urls)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING id
        """, text, photo, video, caption, circle, date_time, button_text, button_url)
        if row:
            return row['id']
        return None

    async def delete_row(self, post_id: int):
        result = await self.connector.execute("""
            DELETE FROM post
            WHERE id = $1
        """, post_id)
        return result == "DELETE 1"

    async def get_bot_row(self, target_date):
        query = await self.connector.fetchrow("""
            SELECT *
            FROM post
            WHERE date_time >= $1
            ORDER BY date_time
        """, target_date)
        return dict(query) if query else None
