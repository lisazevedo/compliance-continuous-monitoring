from datetime import datetime
from typing import List

from pydantic import BaseModel

class CpuBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class CpuCreate(CpuBase):
    host: str
    cpu_usage: str
class Cpu(CpuBase):
    cpu_usage: str
    created_at: datetime
    host: str

    @classmethod
    def from_orm(cls, model):
        return Cpu(
            cpu_usage=model.cpu_usage,
            created_at=model.created_at,
            host=model.ip
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