# Health check endpoint.
#
# Pseudocode (Phase 3, Milestone 3):
#   health endpoint:
#     when GET /health is called:
#       return { "status": "ok" }, HTTP 200
#
# TODO:
# - Create an APIRouter (from fastapi import APIRouter).
# - Define a GET /health route that returns a simple JSON response with
#   HTTP 200.
#
# This should stay intentionally trivial right now — there is no database
# or external API to check yet (those arrive in later milestones).

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok"
    }