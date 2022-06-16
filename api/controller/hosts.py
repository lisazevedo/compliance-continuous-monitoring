import schema
import model

from utils import uuid_alpha
from exceptions import BadRequest, InternalServerError

class HostController:
    def __init__(self, session):
        self.session = session

    def get_hosts(self):
        """
        Retrieves all hosts from database
        Returns
        _______
        host: .schemas.host.hostList
        Raises
        ------
        InternalServerError
            When could not retrieve cpus from database.
        """
        try:
            hosts = (self.session.query(model.Host).all())
            return schema.HostList.from_orm(hosts, len(hosts))
        except:
            raise InternalServerError(code="hostGetAll", message="error when retrieving hosts")

    def create_host(self, host: schema.HostCreate):
        """
        Creates a new Host or update a Host in our database.
        Parameters
        ----------
        host: .schemas.host.hostCreate
        Returns
        _______
        host: .schemas.host.host
        Raises
        ------
        InternalServerError
            When could not create new host row.
        """

        try:

            if not host.ip:
                raise BadRequest(code="createHost", message="missing ip in create host")

            db_host = self.session.query(model.Host).filter_by(ip=host.ip).first()

            if not db_host:
                db_host = model.Host(
                    uuid=uuid_alpha(),
                    ip=host.ip,
                    so_name=host.so_name,
                    so_version=host.so_version
                )
                self.session.add(db_host)
                self.session.flush()

                self.session.commit()

                return schema.Host.from_orm(db_host)
            else:
                update_data = host.dict(exclude_unset=True)
                self.session.query(model.Host).filter_by(uuid=db_host.uuid).update(update_data)
                self.session.commit()

                host = (
                    self.session.query(model.Host)
                    .filter_by(uuid=db_host.uuid)
                    .first()
                )

            return schema.Host.from_orm(host)

        except:
            raise InternalServerError(code="hostCreate", message="error when saving host")

        