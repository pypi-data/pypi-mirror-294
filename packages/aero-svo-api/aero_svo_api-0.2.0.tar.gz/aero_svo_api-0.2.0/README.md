# aero-svo-api  
Unofficial Sheremetyevo International Airport [website](https://www.svo.aero/ru/main) API wrapper 

* Sync/Async usage
* Pydantic models as a result


## Installation
```commandline
pip install aero-svo-api
```
## Available methods
* `get_schedule`  - List of flights for arrival/departure direction in a time range 
* `get_flight`    - Current flight details by its ID 

## Usage example


```python
from datetime import datetime, timedelta
from aero_svo_api import SvoAPI

# each *API instance creates own session with first request if session not provided in constructor
# by default: request.Session for SvoAPI and aiohttp.ClientSession for AsyncSvoAPI

svo_api = SvoAPI()

schedule = svo_api.get_schedule(
    direction='departure',
    date_start=datetime.now(),
    date_end=datetime.now() + timedelta(hours=3),
    # additional parameters (e.g. headers, cookies, ...) forwards to session request
    headers={'User-Agent': 'Custom user-agent'}
)
```


