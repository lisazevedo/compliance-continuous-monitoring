from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class ProcessBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class ProcessPid(ProcessBase):
    pid: str
    user: str

class ProcessCreate(ProcessBase):
    host: str
    processes: List[ProcessPid]

class Process(ProcessBase):
    uuid: str
    host_id: Optional[str]
    user: str
    pid: str
    created_at: datetime

    @classmethod
    def from_orm(cls, model):
        return Process(
            uuid=model.uuid,
            host_id=model.host_id,
            user=model.user,
            pid=model.pid,
            created_at=model.created_at,
        )

class ProcessGet(ProcessBase):
    uuid: str
    user: str
    pid: str
    created_at: datetime
    host: Optional[str]

    @classmethod
    def from_orm(cls, model):
        return ProcessGet(
            uuid=model.uuid,
            user=model.user,
            pid=model.pid,
            created_at=model.created_at,
            host=model.ip
        )

class ProcessList(ProcessBase):
    processes: List[Process]
    total: int

    @classmethod
    def from_orm(cls, models, total):
        return ProcessList(
            processes=[Process.from_orm(model) for model in models],
            total=total
        )

class ProcessListGet(ProcessBase):
    processes: List[ProcessGet]
    total: int

    @classmethod
    def from_orm(cls, models, total):
        return ProcessListGet(
            processes=[ProcessGet.from_orm(model) for model in models],
            total=total
        )