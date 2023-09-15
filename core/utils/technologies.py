import asyncio

import requests
from core.settings import settings


async def read_tech_list():
    tech_list = []
    with open('core/utils/technologies.txt', 'r') as tech_file:
        tech_list = tech_file.read().splitlines()
    return tech_list


async def fetch_job_listings(url):
    response = requests.get(url)

    if response.status_code == 200:
        job_listings = response.json()
        return job_listings
    else:
        with open('logs.txt', 'a') as log_file:
            log_file.write(f'{response.status_code}\n')
        return []


async def extract_keywords_from_sources(sources):
    keywords_list = []

    for source in sources:
        job_listings = await fetch_job_listings(source)

        for job in job_listings:
            keywords = job.get('keywords', [])

            if ' / ' in keywords:
                keys = keywords.split(' / ')
                keywords_list.extend(keys)
            else:
                keywords_list.append(keywords)

    return list(set(keywords_list))


async def save_tech_list(tech_list):
    with open('core/utils/technologies.txt', 'w') as tech_file:
        tech_file.write('\n'.join(tech_list))


async def create_tech_list():
    while True:
        sources = [settings.bots.source]#, settings.bots.source_2]
        keywords_list = await extract_keywords_from_sources(sources)
        tech_list = set(keywords_list)
        await save_tech_list(tech_list)

        await asyncio.sleep(60 * 5)

