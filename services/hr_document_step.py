import uuid

from fastapi import HTTPException, status
from fastapi.logger import logger as log
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from exceptions import BadRequestException, NotFoundException
from models import HrDocumentStep, HrDocumentTemplate
from schemas import (HrDocumentStepCreate, HrDocumentStepRead,
                     HrDocumentStepUpdate)
from services import staff_function_service

from .base import ServiceBase


class HrDocumentStepService(ServiceBase[HrDocumentStep, HrDocumentStepCreate, HrDocumentStepUpdate]):

    def get_by_id(self, db: Session, id: str):

        hr_document_step = super().get(db, id)

        if hr_document_step is None:
            raise NotFoundException(detail=f"Document Step with id: {id} is not found!")

        return hr_document_step

    def get_initial_step_for_template(self, db: Session, template_id: str):

        step = db.query(HrDocumentStep).filter(
            HrDocumentStep.hr_document_template_id == template_id,
            HrDocumentStep.previous_step_id == None
        ).first()

        if step is None:
            raise NotFoundException(detail=f'Initial step for template id: {template_id} is not found!')

        return step

    def get_next_step_from_id(self, db: Session, step_id: str):
        step = db.query(HrDocumentStep).filter(
            HrDocumentStep.previous_step_id == step_id
        ).first()

        return step

    def get_initial_steps(self, db: Session, skip: int, limit: int):

        steps = db.query(self.model).filter(
            self.model.previous_step_id == None
        ).offset(skip).limit(limit).all()

        return steps

    def create_step(self, db: Session, body: HrDocumentStepCreate):
        """
            This code creates a new 'HrDocumentStep' object in the database. The method performs a some check to ensure
            that the new HrDocumentStep is valid according to the application's business logic.

            Here is a summary of what the code does:
            1. If this is the first step in the document template, it creates the new step directly without any checks.
            2. If this is not the first step and if previous step is none then method raises an exception
            3. If this is not the first step, it checks if the previous step has the correct staff_function and raises an exception if it doesn't.
                3.1 If the previous step has staff_function with name 'Утверждающий',
                    it checks staff function of a new step if it not equls to 'Уведомляемый' then method raises an exception
                3.2 If the previous step has staff_function with name 'Уведомляемый' then new step should contains
                    staff_function with the same name. Otherwise, it raises an exception.
            4. If you are trying to create step between existing steps, it changes relationships between there.
        """

        # if there are not some steps in template (1)
        if len(self.get_all_by_document_template_id(db, body.hr_document_template_id)) == 0:
            return super().create(db, body)

        # if previous_step_id is null (2)
        if body.previous_step_id is None:
            raise BadRequestException(
                detail=f"It is not possible to create a HrDocumentStep for HrDocumentTemplate with: {body.hr_document_template_id} id. The reason given is that the HrDocumentStep already has a StaffFunction with the name 'Инициатор'")

        previous_step = self.get_by_id(db, body.previous_step_id)
        staff_function = staff_function_service.get_by_id(db, body.staff_function_id)

        # after step which contains staff_function with 'Утверждающий' name (3.1).
        if previous_step.staff_function.name == "Утверждающий" and staff_function.name != "Уведомляемый":
            raise BadRequestException(
                detail=f"It is not possible to create a HrDocumentStep for HrDocumentTemplate with: {body.hr_document_template_id} id. You can not create HrDocumentStep after HrDocumentStep which has StaffFunction with: 'Утверждающий' name")

        # after step which contains staff_function with 'Уведомляемый' name (3.2).
        if previous_step.staff_function.name == "Уведомляемый" and staff_function.name != "Уведомляемый":
            raise BadRequestException(
                detail=f'После HrDocumentStep с StaffFunction уведомляемого невозможно добавить HrDocumentStep: {staff_function.name}')

        # create a new object of HrDocumentStep
        obj_in_data = jsonable_encoder(body)
        new_step = self.model(**obj_in_data)

        # perform changing relationship (4)
        for i in previous_step.next_step:
            previous_step.next_step.remove(i)
            new_step.next_step.append(i)

        previous_step.next_step.append(new_step)

        db.add(previous_step)
        db.add(new_step)
        db.flush()

        return new_step

    def update_step(self, db: Session, step_id: str, obj_in: HrDocumentStepUpdate):

        step = self.get_by_id(db, step_id)

        # if user is trying to change hr_document_template_id
        if step.hr_document_template_id != obj_in.hr_document_template_id:

            template = db.query(HrDocumentTemplate).filter(HrDocumentTemplate.id == obj_in.hr_document_template_id)
            if template is None:
                raise NotFoundException(detail=f"Document Template with id: {id} is not found!")

            # Change hr_document_template_id to child step is impossible
            if step.previous_step_id is not None:
                raise BadRequestException(f"Child steps can not change template type")

            # getting all steps which template is the same
            steps = db.query(self.model).filter(
                self.model.hr_document_template_id == step.hr_document_template_id
            ).all()

            # update template for all child steps
            for i in steps:
                for j in i.next_step:
                    j.hr_document_template_id = obj_in.hr_document_template_id
                db.add(i)

            step.hr_document_template_id = obj_in.hr_document_template_id

            db.add(step)
            db.flush()
            return self.get_by_id(db, step_id)

        else:
            return super().update(db=db, db_obj=step, obj_in=obj_in)

    def delete_step(self, db: Session, step_id: str):
        step = self.get_by_id(db, step_id)

        # get child step
        child_step = db.query(self.model).filter(
            self.model.previous_step_id == step.id
        ).first()

        # if selected step has child step
        if child_step is not None:
            previous_step = db.query(self.model).filter(
                self.model.id == step.previous_step_id
            ).first()

            if previous_step is not None:
                child_step.previous_step_id = previous_step.id

                previous_step.next_step.append(child_step)
                db.add(previous_step)
            else:
                child_step.previous_step_id = None

            db.add(child_step)

        db.delete(step)
        db.flush()

    def get_all_by_document_template_id(self, db: Session, template_id: uuid.UUID):

        steps = db.query(self.model).filter(
            self.model.hr_document_template_id == template_id
        ).all()

        return steps


hr_document_step_service = HrDocumentStepService(HrDocumentStep)
