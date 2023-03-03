import uuid

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.logger import logger as log
from sqlalchemy.orm import Session

from exceptions import BadRequestException, NotFoundException
from models import (HrDocumentStep, HrDocumentTemplate, DocumentStaffFunction,
                    StaffFunction)
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
            DocumentStaffFunction.priority > 0
        ).first()

        if step is None:
            raise NotFoundException(detail=f'Initial step for template id: {template_id} is not found!')

        return step

    def get_next_step_from_id(self, db: Session, step_id: str) -> HrDocumentStep:
        step = db.query(HrDocumentStep).filter(
            
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
         
        previous_step = self.get_by_id(db, body.previous_step_id)
        staff_function = staff_function_service.get_by_id(db, body.staff_function_id)

        # parent step which contains staff_function with 'Утверждающий' name (3.1)
        # It is not possible to create step after this parent step if staff function of new step is not "Уведомляемый".
        if previous_step.staff_function.name == "Утверждающий" and staff_function.name != "Уведомляемый":
            raise BadRequestException(
                detail=f"It is not possible to create a HrDocumentStep for HrDocumentTemplate with: {body.hr_document_template_id} id. You can not create HrDocumentStep after HrDocumentStep which has StaffFunction with: 'Утверждающий' name")

        # parent step which contains staff_function with 'Уведомляемый' name (3.2).
        # It is not possible to create step after this parent step if staff function of new step is not "Уведомляемый"
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
        """
            This code updates an existing HrDocumentStep object in the database with new data provided in the obj_in parameter.
            The method performs some logic to ensure that the updated HrDocumentStep object is valid according
             to the application's business logic.

            1. Checks selected step exists in database or not. (Selected step is object to update)
            2. If the hr_document_template_id provided in obj_in is different from the current hr_document_template_id
                of the HrDocumentStep object, the code performs some additional logic to update the hr_document_template_id
                for all child steps of the selected step.
                2.1. If the selected step is child step, it raises an error because child steps cannot change the template type.
                2.2. If the selected step is parent step which previous_step_id is 'null' then you should change template type for all child steps.

            Otherwise, this method call update method from super class.
        """

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

            obj_data = jsonable_encoder(self)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)
            for field in obj_data:
                if field in update_data:
                    setattr(self, field, update_data[field])

            db.add(step)
            db.flush()
            return self.get_by_id(db, step_id)

        else:
            return super().update(db=db, db_obj=step, obj_in=obj_in)

    def delete_step(self, db: Session, step_id: str):
        """
            This code deletes a 'HrDocumentStep' object in the database. The method performs a some logics to ensure
            that the object deleted correctly.

            Here are the steps that the code performs:

            1. Checks selected step exists in database or not. (Selected step is object to delete)
            2. If exists you should find child steps
                2.1. If selected step does not have child steps, step deletes as usual
                2.2 If selected step has child step, child step should update his previous_step_id.
                2.3 If selected step has child step and selected step does not have a previous step,
                 then child step should change previous step to 'null'
        """
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
        ).join(self.model.staff_function).order_by(DocumentStaffFunction.priority.asc()).all()

        return steps
    
    def get_next_step_from_priority(self, db: Session, document_id: str, priority: int):

        step = db.query(self.model).filter(
            DocumentStaffFunction.priority > priority
        ).first()

        return step


hr_document_step_service = HrDocumentStepService(HrDocumentStep)
