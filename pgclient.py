import asyncio

import aiopg

dsn = "dbname=aiopg user=postgres password=postgres host=192.168.99.105 port=31718"


async def go():
    pool = await aiopg.create_pool(dsn)
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT 1")
            ret = []
            async for row in cur:
                ret.append(row)
            assert ret == [(1,)]


if __name__ == "__main__":
    asyncio.run(go())
