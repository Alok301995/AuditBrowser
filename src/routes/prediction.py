from fastapi import APIRouter , Request
# For database purposes
from src.services import activity

################################################################################
router = APIRouter()
################################################################################


@router.post("/api2/activity")
def get_activity(request : Request):
    
    body = request.json()
    data = body["data"]
    
    if len(data) > 80:
        act = activity.detect_activity(data)
        return {"activity": activity.detect_activity()}
    else :
        return {"activity": "Not enough data"}


################################################################################