from datetime import datetime
from typing import Optional

from sqlalchemy import asc, desc, func

from api import model, schema
from api.controller.experiments import ExperimentController
from api.controller.utils import uuid_alpha
from api.exceptions import BadRequest, NotFound
from api.utils import now

class CpuController:
    def __init__(self, session):
        self.session = session
    
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
        BadRequest
            When the cpu attributes are invalid.
        """
        store_cpu = (
            self.session.query(model.cpu)
            .filter_by(name=cpu.name)
            .first()
        )
        if store_cpu:
            raise BadRequest(
                code="cpuNameExists",
                message="a cpu with that name already exists",
            )

        cpu = models.cpu(
            uuid=uuid_alpha(),
            name=cpu.name,
            description=cpu.description,
            created_at=now(),
        )
        self.session.add(cpu)
        self.session.flush()

        experiment = schemas.ExperimentCreate(name="Experimento 1")
        self.experiment_controller.create_experiment(
            experiment=experiment, cpu_id=cpu.uuid
        )

        self.session.commit()
        self.session.refresh(cpu)

        return schemas.cpu.from_orm(cpu)

    def get_cpu(self, cpu_id: str):
        """
        Details a cpu from our database.
        Parameters
        ----------
        cpu_id : str
        Returns
        -------
        cpus.schemas.cpu.cpu
        Raises
        ------
        NotFound
            When cpu_id does not exist.
        """
        cpu = (
            self.session.query(models.cpu)
            .filter_by(uuid=cpu_id)
            .filter_by(tenant=self.kubeflow_userid)
            .first()
        )

        if cpu is None:
            raise NOT_FOUND

        return schemas.cpu.from_orm(cpu)

    def update_cpu(self, cpu: schemas.cpuUpdate, cpu_id: str):
        """
        Updates a cpu in our database.
        Parameters
        ----------
        cpu: cpus.schemas.cpu.cpuUpdate
        cpu_id: str
        Returns
        -------
        cpu: cpus.schemas.cpu.cpu
        Raises
        ------
        NotFound
            When cpu_id does not exist.
        BadRequest
            When the cpu attributes are invalid.
        """
        self.raise_if_cpu_does_not_exist(cpu_id)

        stored_cpu = (
            self.session.query(models.cpu)
            .filter_by(name=cpu.name)
            .filter_by(tenant=self.kubeflow_userid)
            .first()
        )
        if stored_cpu and stored_cpu.uuid != cpu_id:
            raise BadRequest(
                code="cpuNameExists",
                message="a cpu with that name already exists",
            )

        update_data = cpu.dict(exclude_unset=True)
        update_data.update({"updated_at": datetime.utcnow()})

        self.session.query(models.cpu).filter_by(uuid=cpu_id).filter_by(
            tenant=self.kubeflow_userid
        ).update(update_data)
        self.session.commit()

        cpu = (
            self.session.query(models.cpu)
            .filter_by(uuid=cpu_id)
            .filter_by(tenant=self.kubeflow_userid)
            .first()
        )

        return schemas.cpu.from_orm(cpu)

    def delete_cpu(self, cpu_id):
        """
        Delete a cpu in our database and in the object storage.
        Parameters
        ----------
        cpu_id : str
        Returns
        -------
        cpus.schemas.message.Message
        Raises
        ------
        NotFound
            When cpu_id does not exist.
        """
        cpu = (
            self.session.query(models.cpu)
            .filter_by(uuid=cpu_id)
            .filter_by(tenant=self.kubeflow_userid)
            .first()
        )

        if cpu is None:
            raise NOT_FOUND

        self.session.delete(cpu)
        self.session.commit()

        return schemas.Message(message="cpu deleted")
