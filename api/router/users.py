from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from controller.users import UserController
import schema
import database

router = APIRouter(
    prefix="/users",
)

@router.get("")
def handle_get_users(
    ip: str,
    session: Session = Depends(database.session_scope)
):
    user_controller = UserController(session)
    users = user_controller.get_users(ip)
    return users

@router.post("")
def handle_post_user(
    req: schema.UserCreate,
    session: Session = Depends(database.session_scope)
):  
    user_controller = UserController(session)
    users = user_controller.create_user(req)
    return users

