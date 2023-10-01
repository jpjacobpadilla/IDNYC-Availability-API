import asyncio
import datetime
import calendar

from scraper import IDNYCScraper


async def main():
    client = IDNYCScraper()

    print('Starting...')

    await client.set_user_token()
    await asyncio.sleep(4)
    
    # Start date is today
    current_date = datetime.date.today()

    # Go two months out
    end_month = current_date.month + 2
    _, last_day = calendar.monthrange(current_date.year, end_month)
    end_date = datetime.date(current_date.year, end_month, last_day)

    all_boroughs = ['3', '2', '4', '5', '1'] 
    all_locations = ['3201', '3298', '3297', '3300', '3150', '3253', '3289', '3293']

    print("Start Date:", current_date)
    print("End Date:", end_date)

    while current_date <= end_date:
        print('\033[38;5;69m' + f'{current_date.strftime("%m/%d/%Y") :-<150}' + '\033[0m')

        string_date = str(current_date)
        one_day = await asyncio.gather(
            *[
                client.fetch_data('Morning', all_locations, all_boroughs, string_date), 
                client.fetch_data('Afternoon', all_locations, all_boroughs, string_date), 
                client.fetch_data('Evening', all_locations, all_boroughs, string_date)
            ],
            return_exceptions=True 
        )

        for task_resp in one_day:
            if isinstance(task_resp, Exception):
                print(task_resp)
                asyncio.sleep(3)
            
            else:
                if client.check_if_there_is_availability(str(task_resp)):
                    print(task_resp)
                else:
                    print("No Availability")

        current_date += datetime.timedelta(days=1)


asyncio.run(main())