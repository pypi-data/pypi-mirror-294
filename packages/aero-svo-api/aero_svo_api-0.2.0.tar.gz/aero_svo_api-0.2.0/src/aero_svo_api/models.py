from datetime import datetime
from decimal import Decimal
from logging import getLogger
from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator, field_validator, AnyHttpUrl, ValidationError


svo_logger = getLogger('svo-api')


class Base(BaseModel):
    @model_validator(mode='before')
    @classmethod
    def empty_str_to_none(cls, data: dict) -> dict:
        return {k: v if v != '' else None for k, v in data.items()}


class Aircraft(Base):
    id: int = Field(alias='aircraft_type_id')
    name: str = Field(alias='aircraft_type_name')


class Country(Base):
    name: str = Field(alias='country')
    region: str


class City(Base):
    name_en: str = Field(alias='city_eng')
    name_ru: str = Field(alias='city')
    timezone: str
    country: Country


class Airport(Base):
    id: int
    iata: str = Field(pattern=r'^[A-Z]{3}$')
    icao: str = Field(pattern=r'^[A-Z]{4}$')
    code_ru: str | None = Field(None, pattern=r'[A-ZА-Я]{3}', alias='rus')
    name: str = Field(alias='airport')
    name_ru: str = Field(alias='airport_rus')
    lat: Annotated[Decimal, Field(max_digits=9, decimal_places=6)] | None = None
    long: Annotated[Decimal, Field(max_digits=9, decimal_places=6)] | None = None
    city: City

    @model_validator(mode='before')
    @classmethod
    def nest_city(cls, data: dict) -> dict:
        if not isinstance(data.get('country'), dict):
            data['city'] = dict(
                city_eng=data.pop('city_eng'),
                city=data.pop('city'),
                timezone=data.pop('timezone'),
                country=dict(
                    country=data.pop('country'),
                    region=data.pop('region'),
                ),
            )

        return data


class Company(Base):
    code: str = Field(pattern='^[A-Z0-9]{2}$')
    name: str
    url_buy: AnyHttpUrl | None = Field(None, alias='onlineBuy')
    url_register: AnyHttpUrl | None = Field(None, alias='onlineRegister')


class Flight(Base):
    id: int = Field(alias='i_id')
    direction: Literal['arrival', 'departure'] = Field(alias='ad')
    company: Company = Field(alias='co')
    number: str = Field(alias='flt')
    date: datetime = Field(alias='dat')
    mar1: Airport
    mar2: Airport
    mar3: Airport | None = None
    mar4: Airport | None = None
    mar5: Airport | None = None
    aircraft: Aircraft
    main_id: int | None = Field(None, alias='main_flight')
    way_time: int
    # check-in
    chin_id: str | None = None
    chin_start: datetime | None = Field(None, alias='t_chin_start')
    chin_end: datetime | None = Field(None, alias='t_chin_finish')
    chin_start_et: datetime | None = Field(None, alias='estimated_chin_start')
    chin_end_et: datetime | None = Field(None, alias='estimated_chin_finish')
    # boarding
    boarding_start: datetime | None = Field(None, alias='t_boarding_start')
    boarding_end: datetime | None = Field(None, alias='t_bording_finish')           # typo in api
    gate_id: str | None = None
    gate_id_prev: str | None = Field(None, alias='old_gate_id')
    # terminal
    term_local: str | None = Field(None, alias='term')
    term_local_prev: str | None = Field(None, alias='old_term')
    # bag belt
    bbel_id: str | None = None
    bbel_id_prev: str | None = Field(None, alias='old_bbel_id')
    bbel_start: datetime | None = None
    bbel_start_et: datetime | None = Field(None, alias='estimated_bag_start')
    bbel_end: datetime | None = Field(None, alias='bbel_finish')
    # schedule
    sked_local: datetime | None= Field(None, alias='t_st')
    sked_other: datetime | None = Field(None, alias='t_st_mar')
    # landing / takeoff
    at_local: datetime | None = Field(None, alias='t_at')
    at_local_et: datetime | None = Field(None, alias='t_et')
    at_other: datetime | None = Field(None, alias='t_at_mar')
    at_other_et: datetime | None = Field(None, alias='marArrivalEt')
    takeoff_et: datetime | None = Field(None, alias='fplTime')
    # departure / arrival to pk
    otpr: datetime | None = Field(None, alias='t_otpr')
    prb: datetime | None = Field(None, alias='t_prb')
    # status
    status_id: int | None = None
    status_code: int | None = None

    @field_validator('direction', mode='before')
    @classmethod
    def convert_direction(cls, value):
        return {'A': 'arrival', 'D': 'departure'}[value]

    @model_validator(mode='before')
    @classmethod
    def nest_aircraft(cls, data: dict) -> dict:
        if not isinstance(data.get('aircraft'), dict):
            data['aircraft'] = dict(aircraft_type_id=data.pop('aircraft_type_id', None),
                                    aircraft_type_name=data.pop('aircraft_type_name', None))
        return data

    @field_validator('takeoff_et', 'at_other_et', mode='before')
    @classmethod
    def remove_invalid_dates(cls, value: str | None) -> datetime | None:
        try:
            datetime.fromisoformat(value)
            return value
        except (ValueError, TypeError):
            return


class Schedule(Base):
    flights: list[Flight] = Field(default_factory=list, alias='items')

    @model_validator(mode='before')
    @classmethod
    def _skip_invalid_flights(cls, data: dict) -> dict:
        flights = []
        for raw_flight in data['items']:
            try:
                valid_flight = Flight.model_validate(raw_flight)
                flights.append(valid_flight)
            except ValidationError as err:
                flight_id = raw_flight.get('i_id')

                extra = {'validation_errors': err.errors(), 'flight_id': flight_id}
                svo_logger.warning(f'Skip flight id={flight_id}\n' + str(err), extra=extra)

        return {'items': flights}
