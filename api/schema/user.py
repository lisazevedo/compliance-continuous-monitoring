from datetime import datetime
from typing import List

from pydantic import BaseModel

class UserBase(BaseModel):
    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class UserCreate(UserBase):
    users: List[str]
    host: str

class User(UserBase):
    uuid: str
    host_id: str
    name: str
    created_at: datetime

    @classmethod
    def from_orm(cls, model):
        return User(
            uuid=model.uuid,
            host_id=model.host_id,
            name=model.name,
            created_at=model.created_at
        )

class UserList(UserBase):
    users: List[User]
    total: int

    @classmethod
    def from_orm(cls, models, total):
        return UserList(
            users=[User.from_orm(model) for model in models],
            total=total
        )