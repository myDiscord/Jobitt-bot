import asyncpg


class Welcome:
    def __init__(self, connector: asyncpg.pool.Pool):
        self.connector = connector

    async def create_welcome_table_if_not_exists(self):
        await self.connector.execute("""
            CREATE TABLE IF NOT EXISTS welcome (

                photo TEXT,
                photo_caption TEXT,
                
                video TEXT,
                video_caption TEXT,
                
                review_photo TEXT[],
                review TEXT
            )
        """)

        count = await self.connector.fetchval("""
        SELECT COUNT(*) FROM welcome
        """)
        if count == 0:
            await self.connector.execute("""
            INSERT INTO welcome DEFAULT VALUES
            """)

    async def update_photo(self, photo: str, photo_caption: str):
        await self.connector.execute("""
            UPDATE welcome
            SET photo = $1, photo_caption = $2
        """, photo, photo_caption)

    async def get_photo(self):
        result = await self.connector.fetchrow("""
            SELECT photo, photo_caption
            FROM welcome
        """)
        return result["photo"], result["photo_caption"]

    async def update_video(self, video: str, video_caption: str):
        await self.connector.execute("""
            UPDATE welcome
            SET video = $1, video_caption = $2
        """, video, video_caption)

    async def get_video(self):
        result = await self.connector.fetchrow("""
            SELECT video, video_caption
            FROM welcome
        """)
        return result["video"], result["video_caption"]

    async def update_review(self, review_photos: list, review: str):
        await self.connector.execute("""
            UPDATE welcome
            SET review_photo = $1, review = $2
        """, review_photos, review)

    async def get_review(self):
        result = await self.connector.fetchrow("""
            SELECT review_photo, review
            FROM welcome
        """)
        return result["review_photo"], result["review"]
