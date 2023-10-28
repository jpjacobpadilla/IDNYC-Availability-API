import random
import asyncio
from datetime import datetime, timedelta
import random
from typing import Any

import httpx
from fake_useragent import UserAgent

from idnyc_api.exceptions import HttpRequestError


class BaseAsyncClient:
    def __init__(self, *, user_agent: str = None, httpx_async_client: httpx.AsyncClient = None, proxy: str = None):
        self.user_agent = user_agent or UserAgent().random
        self.browser_token = self.generate_random_string()
        self.http_client: httpx_async_client or httpx.AsyncClient
        self.proxy = proxy

        self.user_token: str

    async def __aenter__(self):
        self.http_client = httpx.AsyncClient(proxies=self.proxy)

        # Initialize session token
        print('Initializing session token...')
        await self.set_user_token()
        await asyncio.sleep(random.randint(3,5))  # Rest
        print('Initialized session token!')

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.http_client.aclose()

    async def fetch_data(self, start_time: str, locations: list[str], boroughs: list[str], date: str) -> dict[str, Any]:
        assert self.user_token, 'User token is not set.'

        # Define headers
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://a069-idnyconlineportal.nyc.gov",
            "Referer": "https://a069-idnyconlineportal.nyc.gov/IOPWeb/",
            "User-Agent": self.user_agent,
            "Browser_token": self.browser_token,
            "X-Idnyc-User-Token": self.user_token
        }

        data = {
            'startDate': date,
            'startTime': start_time,
            'boroughs': boroughs,
            'enrollmentCenters': locations 
        }

        url = 'https://a069-idnyconlineportal.nyc.gov/IOPWebServices/api/AppointmentApi/GetAvailableTimeSlots' 

        response = await self.http_client.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise HttpRequestError(response.status_code)

        return response.json()
    
    async def set_user_token(self) -> str:
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://a069-idnyconlineportal.nyc.gov",
            "Referer": "https://a069-idnyconlineportal.nyc.gov/IOPWeb/",
            "User-Agent": self.user_agent,
            "Browser_token": self.browser_token,
        }

        data = {'Username': 'admin', 'Password': 'password'}

        url = 'https://a069-idnyconlineportal.nyc.gov/IOPWebServices//api/Login/Login'

        response = await self.http_client.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise HttpRequestError(response.status_code)

        data = response.json()
        self.user_token = data['userToken']

    @staticmethod
    def check_if_there_is_availability(response: dict[str, Any]) -> bool:
        """
        If the response does not match the typical format of a response indicating no available slots, 
        you can assume that slots are available.
        """
        no_slots = "{'$id': '1', 'responseStatusDto': {'$id': '2', 'type': 1, 'errors': {'$id': '3', '$values': []}}, 'responseDataDto': {'$id': '4', 'data': {'$id': '5', '$values': []}}}"
        return response != no_slots

    @staticmethod
    def generate_random_string(length: int = 32) -> str:
        characters = '0123456789abcdef'
        return ''.join(random.choice(characters) for _ in range(length))


class AsyncClient(BaseAsyncClient):
    async def check_availability_range(
        self, start_date: datetime, 
        end_date: datetime, 
        *, 
        request_rest: int = None
    ) -> dict[str, Any]:

        all_boroughs = ['3', '2', '4', '5', '1']
        all_locations = ['3201', '3298', '3297', '3300', '3150', '3253', '3289', '3293']

        current_date = start_date
        while current_date <= end_date:
            print('\033[38;5;69m' + f'{current_date.strftime("%m/%d/%Y") :-<30}' + '\033[0m')

            string_date = current_date.strftime('%m/%d/%Y')
            
            one_day = await asyncio.gather(
                self.fetch_data('Morning', all_locations, all_boroughs, string_date),
                self.fetch_data('Afternoon', all_locations, all_boroughs, string_date),
                self.fetch_data('Evening', all_locations, all_boroughs, string_date),
                return_exceptions=True
            )

            for zone, result in zip(('Morning', 'Afternoon', 'Evening'), one_day):
                if isinstance(result, Exception):
                    print(result)

                else:
                    if self.check_if_there_is_availability(str(result)):
                        print(f'{zone}: {result}')
                    else:
                        print(f'{zone:<10}: No Availability')


            current_date += timedelta(days=1) 
           
            if request_rest is not None:
                await asyncio.sleep(random.uniform(request_rest - request_rest / 2, request_rest + request_rest / 2))

    async def check_availability_day( self, date: datetime) -> dict[str, Any]:
        all_boroughs = ['3', '2', '4', '5', '1']
        all_locations = ['3201', '3298', '3297', '3300', '3150', '3253', '3289', '3293']

        string_date = date.strftime('%m/%d/%Y')

        one_day = await asyncio.gather(
            self.fetch_data('Morning', all_locations, all_boroughs, string_date),
            self.fetch_data('Afternoon', all_locations, all_boroughs, string_date),
            self.fetch_data('Evening', all_locations, all_boroughs, string_date),
            return_exceptions=True
        )

        for zone, result in zip(('Morning', 'Afternoon', 'Evening'), one_day):
            if isinstance(result, Exception):
                print(result)

            else:
                if self.check_if_there_is_availability(str(result)):
                    print(f'{zone}: {result}')
                else:
                    print(f'{zone:<10}: No Availability')