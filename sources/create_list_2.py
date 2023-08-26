import json


def extract_keywords(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        job_listings = json.load(file)

    keywords_list = []

    for job in job_listings:
        keywords = job.get('keywords', [])
        for keyword in keywords:
            keywords_list.extend(keyword.split(' / '))

    unique_keywords = sorted(set(keywords_list))

    with open('tech.txt', 'w', encoding='utf-8') as output_file:
        for keyword in unique_keywords:
            output_file.write(keyword + '\n')

    return unique_keywords


tech = extract_keywords('2.json')
