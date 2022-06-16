from typing import Optional, List

from pydantic import BaseModel

class HostBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class HostCreate(HostBase):
    ip: str
    so_name: Optional[str]
    so_version: Optional[str]

class Host(HostBase):
    uuid: str
    ip: Optional[str]
    so_name: Optional[str]
    so_version: Optional[str]

    @classmethod
    def from_orm(cls, model):
        return Host(
            uuid=model.uuid,
            ip=model.ip,
            so_name=model.so_name,
            so_version=model.so_version,
        )

class HostList(HostBase):
    hosts: List[Host]
    total: int

    @classmethod
    def from_orm(cls, models, total):
        return HostList(
            hosts=[Host.from_orm(model) for model in models],
            total=total
        )