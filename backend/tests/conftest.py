from collections.abc import Generator

import pytest
from sqlalchemy.orm import Session

from app.core.database import SessionLocal


@pytest.fixture
def db_session() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
