# IDNYC-Availability-API

An API to easily check availability for IDNYC appointments across all dates, locations, and times.

Currently, due to the scarcity of available appointments, the bot is designed to print the request response whenever it encounters a response that doesn't match the typical format for an unavailable appointment. In most cases, this would indicate that there might be an available slot.

Have any questions or comments? Contact me at [here](https://jacobpadilla.com/contact).

## Example Usage:

Get Availability of all locations & times for a single day:
```python
import asyncio
from datetime import date

from idnyc_api import AsyncClient


async def main():
    async with AsyncClient() as client:
        await client.check_availability_day(date.today())


if __name__ == '__main__':
    asyncio.run(main())
```

Get Availability of all locations & times for a range of days:
```python
import asyncio
from datetime import date

from idnyc_api import AsyncClient


async def main():
    async with AsyncClient() as client:
        await client.check_availability_range(date(2023, 10, 29), date(2023, 11, 1))


if __name__ == '__main__':
    asyncio.run(main())
```


# To Do List
- Duplicate code in check range & day methods
- Switch to pyproject.toml
- Better Error handling


