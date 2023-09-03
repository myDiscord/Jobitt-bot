import asyncio
from datetime import datetime

import requests
import json

from core.settings import settings


async def update_json():
    url_list = [settings.bots.source]
    filename = "sources/main.json"

    for url in url_list:
        try:
            response = requests.get(url)
            response.raise_for_status()

            with open(filename, 'w') as file:
                json.dump(response.json(), file, indent=4, ensure_ascii=False)

        except requests.exceptions.RequestException as e:
            error_message = f'{datetime.now()} Exception {e}'
            with open('logs.txt', 'a') as log_file:
                log_file.write(error_message + '\n')

    await asyncio.sleep(60 * 1)
    await update_json()
