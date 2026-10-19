import pytest

from pawpal_system import Task


@pytest.mark.parametrize("duration", [0, -5])
def test_invalid_duration_is_rejected(duration):
    with pytest.raises(ValueError):
        Task("Walk", "walk", duration, 1)


@pytest.mark.parametrize("priority", [0, 4, -1])
def test_invalid_priority_is_rejected(priority):
    with pytest.raises(ValueError):
        Task("Walk", "walk", 30, priority)


@pytest.mark.parametrize("frequency", ["monthly", "", "Daily"])
def test_invalid_frequency_is_rejected(frequency):
    with pytest.raises(ValueError):
        Task("Walk", "walk", 30, 1, frequency=frequency)


@pytest.mark.parametrize(
    "time", ["8:00", "25:00", "08:60", "0800", "ab:cd", "", "08:00:00"]
)
def test_invalid_scheduled_time_is_rejected(time):
    with pytest.raises(ValueError):
        Task("Walk", "walk", 30, 1, scheduled_time=time)


@pytest.mark.parametrize("time", ["00:00", "08:05", "23:59", None])
def test_valid_scheduled_time_is_accepted(time):
    assert Task("Walk", "walk", 30, 1, scheduled_time=time).scheduled_time == time
