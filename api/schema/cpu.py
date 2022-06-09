from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, validator

from projects import generic_validators
from projects.schemas.deployment import Deployment
from projects.schemas.experiment import Experiment
from projects.utils import to_camel_case, MAX_CHARS_ALLOWED, FORBIDDEN_CHARACTERS_REGEX, MAX_CHARS_ALLOWED_DESCRIPTION


class CpuBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class Cpu(CpuBase):
    uuid: str
    usage_cpu: str
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