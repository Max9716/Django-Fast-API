from fastapi import APIRouter, Request
from api.services.item_service import run_script
import asyncio
import datetime

router = APIRouter(prefix="/scripts")

ALLOWED_IPS = ["127.0.0.1", "95.24.235.25"]

@router.get("/run/{script_name}")
async def list_items(script_name: str, request: Request):
    client_ip = request.client.host

    if client_ip not in ALLOWED_IPS:
        return {
            "status_code": 403,
            "your_ip": client_ip
        }

    asyncio.create_task(run_script(script_name))

    return {"status": "Прокатило", "Дата": str(datetime.datetime.now())[:19]}

