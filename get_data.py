import asyncio
import datetime
import calendar

from scraper import IDNYCScraper


async def main():
    client = IDNYCScraper()
    await client.set_user_token()
    await asyncio.sleep(4)
    
    # Start date is today
    current_date = datetime.date.today()

    # Go two months out
    end_month = current_date.month + 2
    _, last_day = calendar.monthrange(current_date.year, end_month)
    end_date = datetime.date(current_date.year, end_month, last_day)

    print("Start Date:", current_date)
    print("End Date:", end_date)

    while current_date <= end_date:
        print('\033[38;5;69m' + f'{current_date.strftime("%m/%d/%Y") :-<150}' + '\033[0m')
        print('Morning:')
        print(await client.fetch_data('Morning',['3201', '3298', '3297', '3300', '3150', '3253', '3289', '3293'],['3', '2', '4', '5', '1'], str(current_date)))
        print('Afternoon:')
        print(await client.fetch_data('Afternoon',['3201', '3298', '3297', '3300', '3150', '3253', '3289', '3293'],['3', '2', '4', '5', '1'], str(current_date)))
        print('Evening:')
        print(await client.fetch_data('Evening',['3201', '3298', '3297', '3300', '3150', '3253', '3289', '3293'],['3', '2', '4', '5', '1'], str(current_date)))

        current_date += datetime.timedelta(days=1)


asyncio.run(main())