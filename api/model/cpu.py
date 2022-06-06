"""cpu model."""
from sqlalchemy import Column, ForeignKey, String

from database import Base
from utils import TimeStamp, now


class Cpu(Base):
    __tablename__ = "cpus"
    uuid = Column(String(255), primary_key=True)
    host_id = Column(String(255), ForeignKey("hosts.uuid"), index=True)
    cpu_usage = Column(String(255), index=True)
    created_at = Column(TimeStamp(), nullable=False, default=now())