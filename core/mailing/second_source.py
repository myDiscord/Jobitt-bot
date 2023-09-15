# import re
# import json
# from googletrans import Translator
# from datetime import datetime
#
# import asyncio
#
# from aiogram import Bot
#
# from core.database.db_admins import Admins
# from core.database.db_subscription import Subscription
#
# from core.keyboards.user_inline import ikb_url
# from core.utils.addition_data import job_types, experience, exp_source, english
#
# translator = Translator()
#
#
# async def extract_countries_and_cities(address):
#     cleaned_address = re.sub(r'\s+', ' ', address).replace('+', '')
#     parts = re.split(r'[,(]', cleaned_address)
#
#     countries = []
#     cities = []
#
#     for part in parts:
#         part = part.strip()
#         if part:
#             if '(' in part:
#                 cities.extend([city.strip(')') for city in part.split(',')])
#             else:
#                 if '(' not in cleaned_address:
#                     countries.extend(part.split(','))
#
#     countries = [country.strip() for country in countries]
#     cities = [city.strip() for city in cities]
#
#     return countries, cities
#
#
# async def find_key_by_value(dictionary, search_value):
#     for key, values in dictionary.items():
#         if isinstance(values, list):
#             if search_value in values:
#                 return key.replace(" ", "_")
#             else:
#                 for val in values:
#                     if search_value == val:
#                         return key.replace(" ", "_")
#         elif isinstance(values, str):
#             if search_value == values:
#                 return key.replace(" ", "_")
#     return None
#
#
# async def mailing(telegram_id: int, data_dict: dict, bot: Bot) -> None:
#     if data_dict.get('is_remote'):
#         text_remote = 'Remote work'
#     else:
#         text_remote = 'Office'
#
#     if data_dict.get('company')['website_url']:
#         company = f"<a href={data_dict.get('company')['website_url']}>{data_dict.get('company')['name']}</a>"
#     else:
#         company = f"{data_dict.get('company')['name']}"
#
#     if data_dict.get('salary'):
#         text_salary, salary = f"\n▪️ Salary - {data_dict.get('salary')}", ''
#         if data_dict.get('salary').isdigit():
#             salary = f" #{data_dict.get('salary')}"
#     else:
#         text_salary, salary = '', ''
#
#     if data_dict.get('work_type'):
#         key_found = await find_key_by_value(job_types, data_dict.get('work_type'))
#         if key_found:
#             text_work_type = f"\n▪️ Work type - {key_found}"
#             work_type = f" #{key_found}"
#         else:
#             text_work_type, work_type = '', ''
#     else:
#         text_work_type, work_type = '', ''
#
#     if data_dict.get('website'):
#         website = f" #{data_dict.get('website')}"
#     else:
#         website = ''
#
#     if '/' in data_dict.get('keywords') or ' / ' in data_dict.get('keywords'):
#         keywords = f"#{data_dict['keywords'].split('/')}" if '/' in f"#{data_dict['keywords']}" else data_dict['keywords'].split(' / ')
#         keywords = keywords.replace(' ', '')
#         keyword = ' '.join(keywords)
#     else:
#         keyword = data_dict['keywords'].replace(' ', '')
#         keyword = f" #{keyword}"
#
#     if data_dict.get('address_eng'):
#         countries, cities = await extract_countries_and_cities(data_dict.get('address_eng'))
#         if countries:
#             countries = [country.replace('-', '').replace(' ', '') for country in countries]
#             country = ' '.join([f'#{c}' for c in countries])
#         else:
#             country = ''
#
#         if cities:
#             cities = [city.replace('-', '').replace(' ', '') for city in cities]
#             city = ' '.join([f'#{c}' for c in cities])
#         else:
#             city = ''
#     else:
#         city, country = '', ''
#
#     url = data_dict.get('url')
#     if url.endswith('/'):
#         url += '?utm_source=JOBITT&utm_medium=BOT+&utm_campaign=JOBITT'
#     else:
#         url += '/?utm_source=JOBITT&utm_medium=BOT+&utm_campaign=JOBITT'
#
#     try:
#         await bot.send_message(
#             chat_id=telegram_id,
#             text=f"""
#             {company}
#
# 🔘 {data_dict['name']}
# {text_salary}{text_work_type}
# ▪️ Place of work - {text_remote}
# ▪️ Technologies - {data_dict['keywords']}
#
# {data_dict['short_description']}
#
# #JOBITT{website}{work_type}{salary} {country} {city} {keyword}
#             """,
#             reply_markup=ikb_url(url)
#         )
#     except Exception as e:
#         error_message = f'{datetime.now()} Exception {e}'
#         with open('logs.txt', 'a') as log_file:
#             log_file.write(error_message + '\n')
#
#
# async def check_for_mailing_2(bot: Bot, subscription: Subscription, admins: Admins) -> None:
#     while True:
#         block = await admins.check_block()
#         if block:
#             await asyncio.sleep(60)
#             continue
#
#         last_id = await admins.get_last_processed_data()
#         with open('sources/second.json', 'r', encoding='utf-8') as file:
#             data = json.load(file)
#
#         for row in data:
#             if row['created_at'] == last_id:
#                 await asyncio.sleep(60)
#                 break
#
#             try:
#                 keywords = row['keywords'].split('/') if '/' in row['keywords'] else row['keywords'].split(' / ')
#
#                 all_subscriptions = await subscription.get_all_subscriptions()
#                 for user in all_subscriptions:
#
#                     if keywords and not any(keyword in user['technologies'] for keyword in keywords):
#                         continue
#                     if row['salary'] and row['salary'].isdigit() and user['salary_rate'] > row['salary']:
#                         continue
#
#                     if row['experience']:
#                         for key, val in exp_source.items():
#                             if key in row['experience']:
#                                 exp = exp_source[key]
#                                 if exp > experience[user['experience']]:
#                                     continue
#
#                     if row['english_level']:
#                         if row['english_level'] in english.keys() and english[user['english_lvl']] < english[row['english_level']]:
#                             continue
#                     if job_types[row['work_type']] not in user['job_type']:
#                         continue
#
#                     await mailing(user['telegram_id'], row, bot)
#
#             except Exception as e:
#                 error_message = f'{datetime.now()} Exception {e}'
#                 with open('logs.txt', 'a') as log_file:
#                     log_file.write(error_message + '\n')
#
#         await admins.update_last_processed_data(data[0]['created_at'])
#         await asyncio.sleep(60)
