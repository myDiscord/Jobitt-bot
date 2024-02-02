from typing import List, Dict

from aiomysql import connect, DictCursor


async def create_dict_con():
    connector = await connect(
        host='88.99.59.75',
        port=33005,
        user='root',
        password='Gp73g6Ne3P1',
        db='vacancies',
        cursorclass=DictCursor
    )
    cursor = await connector.cursor()
    return connector, cursor


async def get_keywords():
    con, cur = await create_dict_con()
    await cur.execute("""
        SELECT DISTINCT keywords 
        FROM vacancies;
    """)
    work_types = await cur.fetchall()
    con.close()
    return [row['keywords'] for row in work_types]


async def day_data(job_type: list, technologies: list, experience: str, limit: int = 50) -> List[Dict]:
    con, cur = await create_dict_con()
    await cur.execute("""
        SELECT
            v.id,
            v.name,
            v.salary,
            v.work_type,
            v.english_level,
            v.experience,
            v.is_remote,
            v.short_description,
            v.keywords,
            v.url AS work_url,
            v.created_at,
            v.website,
            c.name AS company_name,
            c.url AS company_url
        FROM
            vacancies v
            LEFT JOIN companies c ON c.id = v.company_id
        WHERE
            (
                (v.work_type IS NULL OR v.work_type IN %s)
                AND (v.keywords IS NULL OR v.keywords IN %s)
                AND (v.experience IS NULL OR v.experience = %s)
                AND c.url IS NOT NULL AND c.url <> ''
            )
        LIMIT %s;
        """, (job_type, technologies, experience, limit))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query


async def new_data(vacancy_id: int) -> List[Dict]:
    con, cur = await create_dict_con()
    await cur.execute(f"""
        SELECT
            v.id,
            v.name,
            v.salary,
            v.work_type,
            v.english_level,
            v.experience,
            v.is_remote,
            v.short_description,
            v.keywords,
            v.url AS work_url,
            v.created_at,
            v.website,
            c.name AS company_name,
            c.url AS company_url
        FROM vacancies v
        LEFT JOIN companies c ON c.id = v.company_id
        WHERE v.id > %s;
        """, (vacancy_id, ))
    query = await cur.fetchall()
    await con.ensure_closed()
    return query
