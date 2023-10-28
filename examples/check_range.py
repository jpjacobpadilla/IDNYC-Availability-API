import asyncio
from datetime import date

from idnyc_api import AsyncClient


async def main():
    async with AsyncClient() as client:
        await client.check_availability_range(date(2023, 10, 29), date(2023, 11, 1))


if __name__ == '__main__':
    asyncio.run(main())