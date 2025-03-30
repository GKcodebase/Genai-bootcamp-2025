from fastapi import APIRouter
from .. import schemas
from datetime import datetime

router = APIRouter()

@router.get("/exercises/{object_id}")
async def get_exercises(object_id: int):
    return {
        "object_id": object_id,
        "exercises": [
            {
                "type": "writing",
                "prompt": "Write the Malayalam word for this object"
            },
            {
                "type": "speaking",
                "prompt": "Pronounce the Malayalam word"
            }
        ],
        "timestamp": datetime.now()
    }