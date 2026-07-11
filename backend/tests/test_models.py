# Milestone 11 — proves the SQLAlchemy model layer actually creates and
# queries real rows against the database. Pseudocode/implementation: TBD.

# tests/test_users.py

import uuid
from datetime import date, datetime, UTC

from sqlalchemy import select

from app.models import Briefing, EconomicEvent

def test_create_and_query_briefing(db_session):
    # Arrange
    briefing = Briefing(
        briefing_date=date(2026, 7, 11),
        title="Daily Economic Briefing",
        summary="A summary of today's major economic developments.",
        status="draft"   
    )

    # Act
    db_session.add(briefing)
    db_session.commit()

    statement = select(Briefing).where(
        Briefing.briefing_date == briefing.briefing_date
    )

    queried_briefing = db_session.scalar(statement)

    # Assert
    assert briefing.id is not None
    assert isinstance (briefing.id, uuid.UUID)
    assert queried_briefing is not None
    assert queried_briefing.briefing_date == briefing.briefing_date
    assert queried_briefing.title == briefing.title 
    assert queried_briefing.summary == briefing.summary 
    assert queried_briefing.status == briefing.status


    # Cleanup is handled by the db_session fixture