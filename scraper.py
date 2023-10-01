import random
import asyncio
import httpx
from fake_useragent import UserAgent

from typing import Any

class IDNYCScraper:
    def __init__(self):
        self.user_agent = UserAgent().random
        self.browser_token = self.generate_random_string()

        self.user_token: str

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

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(response.status_code)

        data = response.json()
        self.user_token = data['userToken']

    async def fetch_data(self, start_time, locations, boroughs, date) -> dict[str, Any]:
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

        async with httpx.AsyncClient() as client:
            response = await client.post( url, headers=headers, json=data)

        if response.status_code != 200:
            raise Exception(response.status_code)

        return response.json()
    
    @staticmethod
    def check_if_there_is_availability(response: dict[str, Any]) -> bool:
        no_slots = "{'$id': '1', 'responseStatusDto': {'$id': '2', 'type': 1, 'errors': {'$id': '3', '$values': []}}, 'responseDataDto': {'$id': '4', 'data': {'$id': '5', '$values': []}}}"

        return response != no_slots