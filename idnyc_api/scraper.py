import random
import asyncio
import httpx
from fake_useragent import UserAgent

from typing import Any

class AsyncClient:
    def __init__(self):
        self.user_agent = UserAgent().random
        self.browser_token = self.generate_random_string()

        self.user_token: str
        self.http_client: httpx.AsyncClient

    async def __aenter__(self):
        self.http_client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.http_client.close()

    @staticmethod
    def generate_random_string(length: int = 32) -> str:
        characters = '0123456789abcdef'
        return ''.join(random.choice(characters) for _ in range(length))

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

    async def check_availability(self, start_date, end_date, *, speed: int = 1) -> dict:
        pass

    async def _fetch_data(self, start_time: str, locations: list[str], boroughs: list[str], date: str) -> dict[str, Any]:
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

        response = await self.http_client.post( url, headers=headers, json=data)

        if response.status_code != 200:
            raise HttpRequestError(response.status_code)

        return response.json()
    
    @staticmethod
    def check_if_there_is_availability(response: dict[str, Any]) -> bool:
        """
        If the response does not match the typical format of a response indicating no available slots, 
        you can assume that slots are available.
        """
        no_slots = "{'$id': '1', 'responseStatusDto': {'$id': '2', 'type': 1, 'errors': {'$id': '3', '$values': []}}, 'responseDataDto': {'$id': '4', 'data': {'$id': '5', '$values': []}}}"

        return response != no_slots
    

class HttpRequestError(Exception):
    """Custom exception for HTTP request errors."""
    
    def __init__(self, status_code: int):
        super().__init__(f'The HTTP request responded with a status code of {status_code}')
