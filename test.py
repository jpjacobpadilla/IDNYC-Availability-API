import asyncio
import datetime
from idnyc_api import AsyncClient

async def main():
    async with AsyncClient() as client:
        date = datetime.date(2023, 10, 29)
        await client.check_availability_day(date)

if __name__ == '__main__':
    asyncio.run(main())