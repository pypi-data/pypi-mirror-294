from enum import StrEnum


class URL(StrEnum):
    TIMETABLE = 'https://www.svo.aero/bitrix/timetable/'
    FLIGHT = 'https://www.svo.aero/bitrix/timetable/{flight_id}/'
