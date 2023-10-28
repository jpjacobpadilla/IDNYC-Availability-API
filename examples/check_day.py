import asyncio
from datetime import date

from idnyc_api import AsyncClient


async def main():
    async with AsyncClient() as client:
        await client.check_availability_day(date.today())


if __name__ == '__main__':
    asyncio.run(main())