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

# Instsallation

Download the code:
```bash
https://github.com/jpjacobpadilla/IDNYC-Availability-API.git
```

Go inside of the cloned repo:
```
cd IDNYC-Availability-API
```

Make some sort of Environment:
```bash
python -m venv venv
source venv/bin/activate
```

Install the package in editable mode so that you can make changes to it:
```bash
pip install -e .
```

# To Do List
- Duplicate code in check range & day methods
- Switch to pyproject.toml
- Better Error handling


