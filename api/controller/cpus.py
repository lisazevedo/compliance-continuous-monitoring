import model
from model import Cpu, Host
import schema

from exceptions import InternalServerError
from utils import uuid_alpha, now
class CpuController:
    def __init__(self, session):
        self.session = session
    
    def get_cpus(self):
        """
        Retrieves all cpus from database
        Returns
        -------
        cpu: .schemas.cpu.cpuList
        Raises
        ------
        InternalServerError
            When could not retrieve cpus from database.
        """

        try:
            cpus = (self.session.query(Cpu)\
                    .join(Host, Cpu.host_id == Host.uuid)\
                    .add_columns(Cpu.cpu_usage, Cpu.created_at, Host.ip)\
                    .order_by(Cpu.created_at.asc()).all())
        
            return schema.CpuList.from_orm(cpus, len(cpus))
        except:
            raise InternalServerError(code="cpuGetAll", message="error when retrieving cpus")

    def create_cpu(self, cpu: schema.CpuCreate):
        """
        Creates a new cpu in our database.
        Parameters
        ----------
        cpu: .schemas.cpu.cpuCreate
        Returns
        -------
        cpu: .schemas.cpu.cpu
        Raises
        ------
        InternalServerError
            When could not create new cpu row.
        """

        try:
            host = self.session.query(model.Host).filter_by(ip=cpu.host).first()

            if not host:
                host = model.Host(
                    uuid=uuid_alpha(),
                    ip=cpu.host
                )
                self.session.add(host)
                self.session.flush()
            
            cpu = model.Cpu(
                uuid=uuid_alpha(),
                cpu_usage=cpu.cpu_usage,
                host_id=host.uuid,
                created_at=now()
            )
            self.session.add(cpu)
            self.session.flush()

            self.session.commit()
            self.session.refresh(cpu)

            return cpu
        except:
            raise InternalServerError(code="cpuCreate", message="error when creating new cpu")