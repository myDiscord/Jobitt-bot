import json
import asyncio
import httpx
import logging

from core.database.db_base import get_keywords

logging.basicConfig(filename='logs.txt', level=logging.ERROR)


async def read_tech_list():
    tech_list = []
    with open('sources/technologies.txt', 'r') as tech_file:
        tech_list = tech_file.read().splitlines()
    return tech_list


async def fetch_job_listings(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        job_listings = response.json()
        return job_listings
    else:
        logging.error(f"HTTP Error {response.status_code} for URL: {url}")
        return []


async def extract_keywords_from_sources(source):
    keywords_list = []

    job_listings = await fetch_job_listings(source)

    for job in job_listings:
        keywords = job.get('keywords', [])

        if ' / ' in keywords:
            keys = keywords.split(' / ')
            keywords_list.extend(keys)
        else:
            keywords_list.append(keywords)

    return list(set(keywords_list))


async def get_keywords_from_base(source: list):
    new_data = []
    for item in source:
        if " / " in item:
            new_data.extend(item.split(" / "))
        else:
            new_data.append(item)

    return new_data


async def save_tech_list(tech_list):
    with open('sources/technologies.txt', 'w') as tech_file:
        tech_file.write('\n'.join(tech_list))


async def create_tech_list():
    while True:
        all_keywords = set()

        first_source = 'http://64.226.76.253/vacancies/'
        keywords_list = await extract_keywords_from_sources(first_source)
        all_keywords.update(keywords_list)

        with open('sources/second.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            keywords_list = [spec["name"] for row in data for spec in row.get("specializations", [])]
            all_keywords.update(keywords_list)

        base_source = await get_keywords()
        keywords_list = await get_keywords_from_base(base_source)
        all_keywords.update(keywords_list)

        await save_tech_list(list(all_keywords))

        await asyncio.sleep(60 * 30)
