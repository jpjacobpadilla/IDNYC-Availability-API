import time
import asyncio

from scraper import IDNYCScraper


async def main():
    client = IDNYCScraper()
    await client.set_user_token()
    await asyncio.sleep(4)
    
    print(await client.fetch_data(1,1,1,1))


asyncio.run(main())