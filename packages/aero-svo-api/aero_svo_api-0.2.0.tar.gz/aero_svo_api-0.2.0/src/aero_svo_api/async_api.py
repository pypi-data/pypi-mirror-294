from typing import Literal, Any
from aiohttp import ClientSession
from abc import ABCMeta, abstractmethod
from datetime import datetime
from functools import cached_property

from . import models
from .urls import URL


class BaseAsyncSvoAPI(metaclass=ABCMeta):
    @abstractmethod
    async def _request(self, url: str, params: dict, **kwargs: Any) -> dict:
        ...

    async def get_schedule(self,
                           direction: Literal['arrival', 'departure'],
                           date_start: datetime,
                           date_end: datetime,
                           per_page: int = 99999,
                           page: int = 0,
                           locale: str = 'ru',
                           raw_return: bool = False,
                           **kwargs
                           ) -> models.Schedule | dict:
        """ List of flights for arrival/departure direction in a time range """
        response = await self._request(
            url=URL.TIMETABLE,
            params=dict(
                direction=direction,
                dateStart=date_start.isoformat(timespec='seconds'),
                dateEnd=date_end.isoformat(timespec='seconds'),
                perPage=per_page,
                page=page,
                locale=locale,
            ),
            **kwargs,
        )
        return models.Schedule.model_validate(response) if raw_return is not True else response

    async def get_flight(self,
                         flight_id: int,
                         locale: str = 'ru',
                         raw_return: bool = False,
                         **kwargs
                         ) -> models.Flight | dict:
        """ Current flight details by its ID """
        response = await self._request(
            url=URL.FLIGHT.format(flight_id=flight_id),
            params=dict(
                locale=locale,
            ),
            **kwargs
        )
        return models.Flight.model_validate(response) if raw_return is not True else response


class AsyncSvoAPI(BaseAsyncSvoAPI):
    def __init__(self, session: ClientSession | None = None) -> None:
        self._session = session

    @cached_property
    def session(self):
        if self._session is None:
            self._session = ClientSession()
        return self._session

    async def _request(self, url: str, params: dict, **kwargs: Any) -> dict:
        response = await self.session.get(url, params=params, **kwargs)
        response.raise_for_status()
        return await response.json()
