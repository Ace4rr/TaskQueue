from datetime import datetime
import pytest
from src.models import Task
from src.exceptions import (
    EmptyTaskIdError,
    InvalidDescriptionError,
    InvalidPriorityError,
    InvalidStatusError,
    InvalidCreatedAtError,
)


def test_task_is_ready_test():
    task = Task(
        id="1",
        description="idks",
        priority=3,
        status="ready",
        created_at=datetime.now(),
    )
    result = task.is_ready
    assert result is True


def test_task_is_not_ready_when_priority_zero():
    task = Task(
        id="1",
        description="idks",
        priority=0,
        status="ready",
        created_at=datetime.now(),
    )
    assert task.is_ready is False


def test_validation_empty_id():
    with pytest.raises(EmptyTaskIdError):
        Task(
            id="",
            description="idks",
            priority=3,
            status="ready",
            created_at=datetime.now(),
        )


def test_validation_description_type():
    with pytest.raises(InvalidDescriptionError):
        Task(
            id="1",
            description=123,
            priority=3,
            status="ready",
            created_at=datetime.now(),
        )


def test_validation_priority_not_int():
    with pytest.raises(InvalidPriorityError):
        Task(
            id="1",
            description="idks",
            priority="23",
            status="ready",
            created_at=datetime.now(),
        )


def test_validation_negative_priority():
    with pytest.raises(InvalidPriorityError):
        Task(
            id="1",
            description="idks",
            priority=-1,
            status="ready",
            created_at=datetime.now(),
        )


def test_validation_invalid_status():
    with pytest.raises(InvalidStatusError):
        Task(
            id="1",
            description="idks",
            priority=3,
            status="something",
            created_at=datetime.now(),
        )


def test_validation_datetime():
    with pytest.raises(InvalidCreatedAtError):
        Task(
            id="1",
            description="idks",
            priority=3,
            status="ready",
            created_at=42,
        )


def test_task_normalizes_status_to_lower():
    task = Task(
        id="1",
        description="idks",
        priority=3,
        status="READY",
        created_at=datetime.now(),
    )
    assert task.status == "ready"


def test_task_short_summary_descriptor():
    task = Task(
        id="1",
        description="a" * 50,
        priority=3,
        status="ready",
        created_at=datetime.now(),
    )
    assert task.short_summary.endswith("...")
    assert len(task.short_summary) == 30