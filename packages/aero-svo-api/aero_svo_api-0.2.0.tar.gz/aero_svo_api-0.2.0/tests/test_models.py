from src.aero_svo_api import models
from .payload import FlightPayload


def test_schedule_skip_invalid():
    valid = FlightPayload().model_dump()
    invalid = {'invalid': 'data'}

    schedule = models.Schedule(items=[valid, invalid])

    assert len(schedule.flights) == 1
    assert schedule.flights[0].id == int(valid['i_id'])
