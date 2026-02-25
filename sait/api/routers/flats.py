from fastapi import APIRouter, Request
import traceback
from api.services.flat_service import get_flats
from api.schemas.flats import FlatsRequest

router = APIRouter(prefix="/flats")

ALLOWED_IPS = ["127.0.0.1", "95.24.235.25"]

@router.post("/")
def flats(request: Request, filters: FlatsRequest):
    client_ip = request.client.host

    if client_ip not in ALLOWED_IPS:
        return {
            "status_code": 403,
            "your_ip": client_ip
        }
    try:
        data = get_flats(filters.id_complex)
        return {
            "status": "ok",
            "count": len(data),
            "data": data
        }
    except Exception as e:
        return {"status": "error", "message": str(e), "trace": traceback.format_exc()}

