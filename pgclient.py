import asyncio
import os

import aiopg
import rapidtables

hostname = os.environ["NODE_IP"]
port = os.environ["NODE_PORT"]
dsn = f"dbname=postgres user=postgres password=postgres host={hostname} port={port}"

factbook_select_all_query = """
SELECT year, date, shares, trades, dollars
FROM factbook
"""


query = factbook_select_all_query


async def go():
    pool = await aiopg.create_pool(dsn)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(query)
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
