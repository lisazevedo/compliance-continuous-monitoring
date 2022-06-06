"""host model."""
from sqlalchemy import Column, String
from database import Base

class Host(Base):
    __tablename__ = "hosts"
    uuid = Column(String(255), primary_key=True)
    ip = Column(String(255), index=True)
    so_name = Column(String(255), index=True)
    so_version = Column(String(255), index=True)
