"""process model."""
from sqlalchemy import Column, ForeignKey, String

from database import Base
from utils import TimeStamp, now


class Process(Base):
    __tablename__ = "processes"
    uuid = Column(String(255), primary_key=True)
    host_id = Column(String(255), ForeignKey("hosts.uuid"), index=True)
    user_id = Column(String(255), ForeignKey("users.uuid"), index=True)
    pid = Column(String(255), index=True)
    created_at = Column(TimeStamp(), nullable=False, default=now())