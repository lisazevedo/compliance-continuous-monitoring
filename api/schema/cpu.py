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
    host: str
    created_at: datetime

    @classmethod
    def from_orm(cls, model):
        return Cpu(
            uuid=model.uuid,
            usage_cpu=model.usage_cpu,
            host=model.hosts,
            created_at=model.created_at,
        )