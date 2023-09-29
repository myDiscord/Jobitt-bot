from aiomysql import connect, DictCursor


async def create_dict_con():
    connector = await connect(
        host='64.226.76.253',
        port=3306,
        user='admin',
        password='Gp73g6Ne3P1',
        db='vacancies',
        cursorclass=DictCursor
    )
    cursor = await connector.cursor()
    return connector, cursor


async def get_vacancies(created_at):
    con, cur = await create_dict_con()
    await cur.execute("""
        SELECT 
            v.id, v.name, v.salary, v.work_type, v.english_level, v.experience, v.is_remote, 
            v.short_description, v.address_eng, v.keywords, v.created_at,
            c.name as company_name, c.url, c.website_url
        FROM vacancies v
        LEFT JOIN companies c ON v.company_id = c.id 
        WHERE c.url IS NOT NULL AND c.url <> '' AND v.created_at > current_date - interval '1 month'
        ORDER BY v.created_at DESC;
        """, (created_at,))
    query = await cur.fetchall()
    con.close()
    return query


async def get_keywords():
    con, cur = await create_dict_con()
    await cur.execute("""
        SELECT DISTINCT keywords 
        FROM vacancies;
    """)
    work_types = await cur.fetchall()
    con.close()
    return [row['keywords'] for row in work_types]


async def get_vacancies_by_interest(created_at):
    con, cur = await create_dict_con()
    await cur.execute("""
        SELECT 
            v.id, v.name, v.salary, v.work_type, v.english_level, v.experience, v.is_remote, 
            v.short_description, v.address_eng, v.keywords, v.created_at,
            c.name as company_name, c.url, c.website_url
        FROM vacancies v
        LEFT JOIN companies c ON v.company_id = c.id 
        WHERE c.url IS NOT NULL AND c.url <> '' AND v.created_at < %s
        ORDER BY v.created_at DESC;
        """, (created_at,))
    query = await cur.fetchall()
    con.close()
    return query
