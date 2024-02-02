import asyncio
import json

from core.database.db_base import get_keywords


async def make_tech_list():
    while True:
        keywords = await get_keywords()
        with open('core/utils/keywords.json', 'w', encoding='utf-8') as json_file:
            json.dump(keywords, json_file, ensure_ascii=False, indent=4)

        await asyncio.sleep(60 * 60)
