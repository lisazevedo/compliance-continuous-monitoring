from typing import List, Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

import database

from controller.cpus import CpuController
import schema as schemas

router = APIRouter(
    prefix="/cpus",
)


@router.post("")
def handle_post_cpus(
    cpu: schemas.CpuCreate,
    session: Session = Depends(database.session_scope),
):
    cpu_controller = CpuController(session)
    cpus = cpu_controller.create_cpu(cpu)
    return cpus







