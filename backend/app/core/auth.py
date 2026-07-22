from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

clerk_config = ClerkConfig(
    jwks_url=settings.clerk_jwks_url,
)

clerk_auth_guard = ClerkHTTPBearer(config=clerk_config)


def get_current_user(
    credentials: Any = Depends(clerk_auth_guard),
    db: Session = Depends(get_db),
) -> User:
    """
    Authenticate the request using Clerk and return the corresponding local database user.

    Creates the local user record the first time the user accesses the application.
    """
    decoded_token = credentials.decoded or {}

    clerk_user_id = decoded_token.get("sub")

    if not isinstance(clerk_user_id, str) or not clerk_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clerk user ID is missing from the session token",
        )

    email = decoded_token.get("email")

    if not isinstance(email, str) or not email.strip():
        email = None
    else:
        email = email.strip()

    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()

    if user is None:
        user = User(clerk_user_id=clerk_user_id, email=email)

        db.add(user)
        db.commit()

    return user
