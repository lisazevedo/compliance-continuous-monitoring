from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/hosts",
)

@router.post("")
def handle_post():
    return "pong"

