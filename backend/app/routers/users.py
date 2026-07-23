# from fastapi import APIRouter, Depends
# from sqlalchemy import text
# from sqlalchemy.orm import Session

# from app.core.database import get_db
# from app.schemas.health import HealthResponse

from fastapi import APIRouter, Depends 
from app.core.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserPreferences

from sqlalchemy.orm import Session
from app.core.database import get_db

router = APIRouter()


# @router.get("/health", response_model=HealthResponse)
# def health(db: Session = Depends(get_db)) -> HealthResponse:
#     db.execute(text("SELECT 1"))
#     return HealthResponse(status="ok")

@router.get("/users/me/preferences", response_model=UserPreferences)
def get_preferences(user: User = Depends(get_current_user)) -> UserPreferences:
    return UserPreferences(
        category=user.category,
        additional_topics=user.additional_topics
    )

@router.put("/users/me/preferences", response_model=UserPreferences)
def put_preferences(
    body: UserPreferences,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserPreferences:
    user.category = body.category
    user.additional_topics = body.additional_topics 

    db.commit()

    return UserPreferences(
        category=user.category,
        additional_topics=user.additional_topics 
    )


    

    