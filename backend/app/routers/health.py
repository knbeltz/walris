# This should stay intentionally trivial right now — there is no database
# or external API to check yet (those arrive in later milestones).

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
