from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import BaseModel, validator

class CpuBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class CpuCreate(CpuBase):
    host: str
    cpu_usage: str
class Cpu(CpuBase):
    uuid: str
    cpu_usage: str
    host_id: str
    created_at: datetime

    @classmethod
    def from_orm(cls, model):
        return Cpu(
            uuid=model.uuid,
            cpu_usage=model.cpu_usage,
            host_id=model.host_id,
            created_at=model.created_at,
        )

class CpuList(CpuBase):
    cpus: List[Cpu]
    total: int

    @classmethod
    def from_orm(cls, models, total):
        return CpuList(
            cpus=[Cpu.from_orm(model) for model in models],
            total=total
        )