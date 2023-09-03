import requests

from core.settings import settings

tech_list = []


async def fetch_job_listings(url):
    response = requests.get(url)

    if response.status_code == 200:
        job_listings = response.json()
        return job_listings
    else:
        with open('logs.txt', 'a') as log_file:
            log_file.write(f'{response.status_code}\n')
        return []


async def extract_keywords(job_listings):
    keywords_list = []

    for job in job_listings:
        keywords = job.get('keywords', [])

        if ' / ' in keywords:
            keys = keywords.split(' / ')
            keywords_list.extend(keys)
        else:
            keywords_list.append(keywords)

    return list(set(keywords_list))


async def create_tech_list():
    url = settings.bots.source
    job_listings = await fetch_job_listings(url)

    if job_listings:
        keywords_list = await extract_keywords(job_listings)
        for keyword in keywords_list:
            if keyword not in tech_list:
                tech_list.append(keyword)
