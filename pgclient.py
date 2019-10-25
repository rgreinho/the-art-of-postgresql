import asyncio
import datetime
import os

import aiopg
import rapidtables

hostname = os.environ["PGHOST"]
port = os.environ["PGPORT"]
dsn = f"dbname=postgres user=postgres password=postgres host={hostname} port={port}"


def fetch_all():
    query = """
    SELECT year, date, shares, trades, dollars
        FROM factbook
    """
    return query, None


def fetch_month_data(month, year):
    parameters = {"date": datetime.date(year, month, 1)}

    query = """
    SELECT year, date, shares, trades, dollars
        FROM factbook
    WHERE date >= %(date)s::date
        AND date < %(date)s::date + INTERVAL '1 month'
    ORDER BY date
    """
    return query, parameters


query_and_params = fetch_month_data(8, 2017)


async def go():
    pool = await aiopg.create_pool(dsn)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(*query_and_params)
            headers = [d.name for d in cur.description]
            data = []
            async for row in cur:
                data.append(dict(zip(headers, row)))
    pool.close()
    await pool.wait_closed()
    print("ALL DONE")
    rapidtables.print_table(data)


if __name__ == "__main__":
    asyncio.run(go())
