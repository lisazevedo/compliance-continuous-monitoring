"""user model."""
from sqlalchemy import Column, ForeignKey, String

from database import Base
from utils import TimeStamp, now


class User(Base):
    __tablename__ = "users"
    uuid = Column(String(255), primary_key=True)
    host_id = Column(String(255), ForeignKey("hosts.uuid"), index=True)
    name = Column(String(255), index=True)
    created_at = Column(TimeStamp(), nullable=False, default=now())