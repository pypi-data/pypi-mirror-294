from datetime import datetime, timedelta, timezone

import pytest
from tenacity import retry, stop_after_attempt

from src.aero_svo_api import AsyncSvoAPI


@pytest.mark.usefixtures('throttle',)
class TestAsyncSvoAPI:
    @retry(stop=stop_after_attempt(3))
    async def test_get_schedule(self):
        date_start = datetime.now(tz=timezone.utc)
        date_end = date_start + timedelta(hours=3)

        response = await AsyncSvoAPI().get_schedule(
            'departure',
            date_start=date_start,
            date_end=date_end
        )

        assert len(response.flights) > 0
        assert {flight.direction for flight in response.flights} == {'departure'}

        sked_times = sorted((flight.sked_local for flight in response.flights))
        assert sked_times[0] >= date_start
        assert sked_times[1] <= date_end

    @retry(stop=stop_after_attempt(3))
    async def test_get_schedule_raw(self):
        response = await AsyncSvoAPI().get_schedule(
            direction='arrival',
            date_start=datetime.now(),
            date_end=datetime.now() + timedelta(hours=3),
            raw_return=True,
        )

        assert len(response['items']) == response['pagination']['totalItems'] > 1
        assert response['pagination']['pageCount'] == 99999
        assert response['pagination']['curPage'] == 1

    @retry(stop=stop_after_attempt(3))
    async def test_get_flight(self):
        response = await AsyncSvoAPI().get_flight(8990982)
        assert response.id == 8990982
        assert response.mar1.name == 'Нижневартовск'

    @retry(stop=stop_after_attempt(3))
    async def test_get_flight_raw(self):
        response = await AsyncSvoAPI().get_flight(8990983, raw_return=True)
        assert response['i_id'] == '8990983'
