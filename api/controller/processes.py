import schema
import model
from model import Process, Host

from exceptions import InternalServerError, BadRequest, NotFound
from utils import uuid_alpha, now

class ProcessController:
    def __init__(self, session):
        self.session = session

    def get_processes(self, ip: str):
        """
        Retrieves all processes from database by host ip
        Query
        ----------
        ip: str
        Returns
        -------
        user: .schemas.process.ProcessList
        Raises
        ------
        BadRequest
            When ip is not passed through request query
        NotFound
            When could not find host with ip address
        """
        if not ip:
            raise BadRequest(code="processGet", message="missing host parameter in get processes")

        host = self.session.query(Host).filter_by(ip=ip).first()

        if not host:
            raise NotFound(code="processGet", message="could not find host with this ip")

        processes = self.session.query(Process)\
                    .filter_by(host_id=host.uuid)\
                    .join(Host, Process.host_id == Host.uuid)\
                    .add_columns(Process.uuid, Process.user, Process.pid, Process.created_at, Host.ip)\
                    .order_by(Process.created_at.asc()).all()

        return schema.ProcessListGet.from_orm(processes, len(processes))

    def create_processes(self, req: schema.ProcessCreate):
        """
        Creates new processes in our database
        Parameters
        ----------
        req: .schemas.process.processCreate
        Returns
        -------
        processes: .schemas.process.processList
        Raises
        ------
        BadRequest
            When ip is not passed through request query
        InternalServerError
            When could not create new processes
        """
        try:
            if not req.host:
                raise BadRequest(code="processCreate", message="missing host parameter in create processes")

            host = self.session.query(model.Host).filter_by(ip=req.host).first()

            if not host:
                host = model.Host(
                    uuid=uuid_alpha(),
                    ip=req.host
                )
                self.session.add(host)
                self.session.flush()

            created_processes = []

            for process in req.processes:
                new_process = model.Process(
                    uuid=uuid_alpha(),
                    host_id=host.uuid,
                    user=process.user,
                    pid=process.pid,
                    created_at=now()
                )
                created_processes.append(new_process)
                self.session.add(new_process)
                self.session.flush()

            self.session.commit()
            return schema.ProcessList.from_orm(created_processes, len(created_processes))

        except:
            raise InternalServerError(code="processCreate", message="error when creating new processes")
