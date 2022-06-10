import model as models
import schema as schemas

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
            cpus = (self.session.query(models.Cpu).order_by(models.Cpu.created_at.asc()).all())
            return schemas.CpuList.from_orm(cpus, len(cpus))
        except:
            raise InternalServerError(code="cpuGetAll", message="error when retrieving cpus")

    def create_cpu(self, cpu: schemas.CpuCreate):
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
            host = self.session.query(models.Host).filter_by(ip=cpu.host).first()

            if not host:
                host = models.Host(
                    uuid=uuid_alpha(),
                    ip=cpu.host
                )
                self.session.add(host)
                self.session.flush()
            
            cpu = models.Cpu(
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