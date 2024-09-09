from fastapi import APIRouter, Request

from common.utils.system import System

router = APIRouter(tags=["Monitor"])


@router.get("/monitor")
def monitor():
    info = System().GetSystemAllInfo()
    return info
