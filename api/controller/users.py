import model
from model import User, Host
import schema

from exceptions import InternalServerError, BadRequest, NotFound
from utils import uuid_alpha, now

class UserController:
    def __init__(self, session):
        self.session = session

    def get_users(self, ip: str):
        """
        Retrieves all users from database by host ip
        Query
        ----------
        ip: str
        Returns
        -------
        user: .schemas.user.userList
        Raises
        ------
        BadRequest
            When ip is not passed through request query
        NotFound
            When could not find host with ip address
        """
        if not ip:
            raise BadRequest(code="userGet", message="missing host parameter in get users")

        host = self.session.query(Host).filter_by(ip=ip).first()

        if not host:
            raise NotFound(code="userGet", message="could not find host with this ip")

        users = self.session.query(User)\
                .filter_by(host_id=host.uuid)\
                .join(Host, User.host_id == Host.uuid)\
                .add_columns(User.uuid, User.name, User.created_at, Host.ip)\
                .order_by(User.created_at.asc()).all()

        return schema.UserListGet.from_orm(users, len(users))

    def create_user(self, req: schema.UserCreate):
        """
        Creates a new user in our database
        Parameters
        ----------
        user: .schemas.user.userCreate
        Returns
        -------
        user: .schemas.user.userList
        Raises
        ------
        InternalServerError
            When could not create new user row.
        """
        try:
            host = self.session.query(model.Host).filter_by(ip=req.host).first()

            if not host:
                host = model.Host(
                    uuid=uuid_alpha(),
                    ip=req.host
                )
                self.session.add(host)
                self.session.flush()

            created_users = []

            for user in req.users:
                new_user = model.User(
                    uuid=uuid_alpha(),
                    name=user,
                    host_id=host.uuid,
                    created_at=now()
                )
                created_users.append(new_user)
                self.session.add(new_user)
                self.session.flush()

            self.session.commit()

            return schema.UserList.from_orm(created_users, len(created_users))
        except: 
            raise InternalServerError(code="userCreate", message="error when creating new user")