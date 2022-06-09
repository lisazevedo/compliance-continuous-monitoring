from typing import List, Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session

import database

router = APIRouter(
    prefix="/cpus",
)


@router.post("")
def handle_post_cpus(
    # request_schema: projects.schemas.project.ProjectListRequest,
    session: Session = Depends(database.session_scope),
):
    return session







