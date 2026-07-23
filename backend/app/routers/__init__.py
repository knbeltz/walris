# Future versioned endpoints (briefings, events, notifications, admin) get
# registered on this router — it's included in the app now, with no routes
# yet, so the /v1 prefix is already solved when the first real one arrives.
from fastapi import APIRouter
from app.routers.users import router as users_router

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(users_router)
