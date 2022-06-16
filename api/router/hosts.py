from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

from controller.hosts import HostController

import database
import schema

router = APIRouter(
    prefix="/hosts",
)

@router.get("")
def handle_get_all_hosts(
    session: Session = Depends(database.session_scope)
):
    host_controller = HostController(session)
    hosts = host_controller.get_hosts()
    return hosts

@router.post("")
def handle_post_host(
    host: schema.HostCreate,
    session: Session = Depends(database.session_scope)
):
    host_controller = HostController(session)
    hosts = host_controller.create_host(host)
    return hosts

