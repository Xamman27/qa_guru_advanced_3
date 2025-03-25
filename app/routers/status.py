from fastapi import APIRouter
from app.database.engine import check_availability
from app.models.models import AppStatus


router = APIRouter()
@router.get('/api/status', response_model=AppStatus)
def get_status():
    return AppStatus(database=check_availability())