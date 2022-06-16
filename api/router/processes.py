from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from controller.processes import ProcessController
import schema
import database

router = APIRouter(
    prefix="/processes",
)

@router.get("")
def handle_get_processes(
    ip: str,
    session: Session = Depends(database.session_scope)
):
    process_controller = ProcessController(session)
    processes = process_controller.get_processes(ip)
    return processes

@router.post("")
def handle_post_processes(
    req: schema.ProcessCreate,
    session: Session = Depends(database.session_scope)
):
    process_controller = ProcessController(session)
    processes = process_controller.create_processes(req)
    return processes

