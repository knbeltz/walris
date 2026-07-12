# Milestone 11 — proves the SQLAlchemy model layer actually creates and
# queries real rows against the database. Pseudocode/implementation: TBD.

import uuid
from datetime import UTC, date, datetime

from sqlalchemy import select

from app.models import Briefing, EconomicEvent


def test_create_and_query_briefing(db_session):
    # Arrange
    briefing = Briefing(
        briefing_date=date(2026, 7, 11),
        title="Daily Economic Briefing",
        summary="A summary of today's major economic developments.",
        status="draft",
    )

    # Act
    db_session.add(briefing)
    db_session.commit()

    queried_briefing = db_session.scalar(
        select(Briefing).where(Briefing.briefing_date == briefing.briefing_date)
    )

    # Assert
    assert briefing.id is not None
    assert isinstance(briefing.id, uuid.UUID)
    assert queried_briefing is not None
    assert queried_briefing.briefing_date == briefing.briefing_date
    assert queried_briefing.title == briefing.title
    assert queried_briefing.summary == briefing.summary
    assert queried_briefing.status == briefing.status

    # Cleanup
    db_session.delete(queried_briefing)
    db_session.commit()


def test_create_and_query_economic_event(db_session):
    # Arrange
    briefing = Briefing(
        briefing_date=date(2026, 7, 11),
        title="Daily Economic Briefing",
        summary="A summary of today's major economic developments.",
        status="draft",
    )

    db_session.add(briefing)
    db_session.commit()

    event = EconomicEvent(
        briefing_id=briefing.id,
        external_event_id="test-event-001",
        event_name="1",
        country="Germany",
        release_time=datetime(2026, 7, 11, 13, 30, tzinfo=UTC),
        actual_value=2.2,
        forecast_value=2.3,
        previous_value=2.1,
        unit="2",
        source="3",
    )

    # Act
    db_session.add(event)
    db_session.commit()

    queried_event = db_session.scalar(
        select(EconomicEvent).where(EconomicEvent.briefing_id == briefing.id)
    )

    # Assert
    assert queried_event is not None
    assert queried_event.briefing_id == briefing.id
    assert queried_event.external_event_id == event.external_event_id
    assert queried_event.country == event.country
    assert queried_event.actual_value == event.actual_value
    assert queried_event.forecast_value == event.forecast_value
    assert queried_event.previous_value == event.previous_value
    assert queried_event.unit == event.unit

    # Cleanup
    db_session.delete(queried_event)
    db_session.flush()
    db_session.delete(briefing)
    db_session.commit()
