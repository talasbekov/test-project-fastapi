import uuid

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List, Union, Dict

from exceptions import NotFoundException
from models import (
    HrDocumentTemplate,
    HrDocumentStep,
    DocumentStaffFunction,
    User,
    Notification,
    HrDocumentTemplateEnum,
    StaffDivisionEnum,
    
)
from models.association import staff_unit_function
from schemas import (
    HrDocumentTemplateCreate,
    HrDocumentTemplateUpdate,
    HrDocumentTemplateRead,
    DocumentStaffFunctionCreate,
    HrDocumentStepCreate,
    SuggestCorrections,
    NotificationCreate,
)
from .base import ServiceBase
from services import (
    hr_document_step_service,
    document_staff_function_service,
    notification_service,
    staff_unit_service,
    staff_division_service,
    categories,
    BaseCategory,
)
from ws import notification_manager


class HrDocumentTemplateService(ServiceBase[HrDocumentTemplate, HrDocumentTemplateCreate, HrDocumentTemplateUpdate]):

    def create_template(self, db: Session, body: HrDocumentTemplateCreate, role: str) -> HrDocumentTemplateRead:
        current_user_staff_unit_id = staff_unit_service.get_by_id(db, role)

        obj_in_data = jsonable_encoder(body)
        hr_document_template = self.model(**obj_in_data)

        hr_document_template.maintainer_id = current_user_staff_unit_id.id

        db.add(hr_document_template)
        db.flush()

        return hr_document_template

    def get_by_id(self, db: Session, id: str) -> HrDocumentTemplate:
        hr_document_template = super().get(db, id)
        if hr_document_template is None:
            raise NotFoundException(detail=f'HrDocumentTemplate with id: {id} is not found!')
        return hr_document_template

    def get_steps_by_document_template_id(self, db: Session, document_template_id: str, user_id: uuid.UUID) -> dict[str, Union[uuid.UUID, Dict[int, uuid.UUID]]]:

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise NotFoundException(detail=f'User with id: {user_id} is not found!')

        initial_step = hr_document_step_service.get_initial_step_for_template(db, document_template_id)

        all_steps = hr_document_step_service.get_all_by_document_template_id(db, document_template_id)

        all_functions = db.query(DocumentStaffFunction).filter(
            HrDocumentStep.hr_document_template_id == document_template_id,
            DocumentStaffFunction.priority != 1
        ).join(HrDocumentStep.staff_function).order_by(DocumentStaffFunction.priority.asc()).all()
        
        all_steps.remove(initial_step)

        steps = {}
        for function, step in zip(all_functions, all_steps):
            function: DocumentStaffFunction

            if step.is_direct_supervisor is not None:
                steps[str(function.priority)] = self.get_all_supervisors(db, step.id, step.is_direct_supervisor, document_template_id, user)
                continue
            if step.category is not None:
                category: BaseCategory  = categories.get(step.category, None)
                if category is None:
                    raise NotFoundException(detail=f'Category with id: {step.category} is not found!')
                steps[str(function.priority)] = category.handle(db)
                continue
            staff_units_ids = [unit.id for unit in function.staff_units]
            user = db.query(User).filter(
                User.staff_unit_id.in_(staff_units_ids)
            ).first()
            steps[str(function.priority)] = str(user.id)
        return steps

    def get_all_by_name(self, db: Session, name: str, skip: int, limit: int):
        if name:
            return db.query(HrDocumentTemplate).filter(
                HrDocumentTemplate.is_active == True,
                (
                    HrDocumentTemplate.name.ilike(f'%{name}%') |
                    HrDocumentTemplate.description.ilike(f'%{name}%')
                )
            ).filter(HrDocumentTemplate.is_visible == True).offset(skip).limit(limit).all()
        return self.get_all_active(db, skip, limit)

    def get_all_active(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[HrDocumentTemplateRead]:
        return (
            db.query(HrDocumentTemplate)
            .filter(HrDocumentTemplate.is_active == True)
            .filter(HrDocumentTemplate.is_visible == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_archived(self, db: Session, skip: int, limit: int):
        return (
            db.query(self.model)
            .filter(self.model.is_active == False)
            .filter(self.model.is_visible == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def duplicate(self, db: Session, id: str):
        template = self.get_by_id(db, id)
        new_template =self.create(
            db,
            HrDocumentTemplateCreate(
                name=template.name if template.name is None else template.name + " (Копия)",
                nameKZ=template.nameKZ + " (Копия)",
                path=template.path,
                pathKZ=template.pathKZ,
                subject_type=template.subject_type,
                properties=template.properties,
                description=template.description,
                actions=template.actions,
                is_visible=template.is_visible,
            )
        )
        steps = hr_document_step_service.get_all_by_document_template_id(db, template.id)
        for step in steps:
            staff_function: DocumentStaffFunction = step.staff_function
            new_staff_function = document_staff_function_service.create(
                db,
                DocumentStaffFunctionCreate(
                    name=staff_function.name + " (Копия)",
                    nameKZ=staff_function.nameKZ if staff_function.nameKZ is None else staff_function.nameKZ + " (Копия)",
                    hours_per_week=staff_function.hours_per_week,
                    priority=staff_function.priority,
                    role_id=staff_function.role_id,
                    jurisdiction_id=staff_function.jurisdiction_id,
                )
            )
            new_staff_function.staff_units = staff_function.staff_units
            new_step = hr_document_step_service.create(
                db,
                HrDocumentStepCreate(
                    hr_document_template_id=new_template.id,
                    staff_function_id=new_staff_function.id,
                )
            )
            db.add(new_staff_function)
        db.add(new_template)
        return new_template

    async def suggest_corrections(self, db: Session, body: SuggestCorrections, current_user_id: uuid.UUID):
        template = self.get_by_id(db, body.hr_document_template_id)
        for i in template.maintainer.actual_users:
            db.add(notification_service.create(
                db,
                NotificationCreate(
                    message=template.name+body.text,
                    sender_id=current_user_id,
                    receiver_id=i.id
                    )
                )
            )
            await notification_manager.broadcast(body.text, i.id)

    def get_staff_list(self, db: Session):
        res = db.query(self.model).filter(self.model.name == HrDocumentTemplateEnum.STAFF_LIST.value).first()
        if res is None:
            raise NotFoundException(detail=f'HrDocumentTemplate with name: {HrDocumentTemplateEnum.STAFF_LIST.value} is not found!')
        return res

    def get_staff_unit(self, db: Session):
        res = db.query(self.model).filter(self.model.name == HrDocumentTemplateEnum.STAFF_UNIT.value).first()
        if res is None:
            raise NotFoundException(detail=f'HrDocumentTemplate with name: {HrDocumentTemplateEnum.STAFF_UNIT.value} is not found!')
        return res

    def get_all(self, db: Session, ids: List[uuid.UUID]):
        return db.query(self.model).filter(
            self.model.id.in_(ids),
            self.model.is_active == True,
            self.model.is_visible == True,
            ).all()

    def get_all_supervisors(self, db: Session, step_id: uuid.UUID, is_direct: bool, template_id: uuid.UUID, user: User):
        count = 1
        all_steps = {}
        if is_direct:
            if user.staff_unit.staff_division.leader_id != user.staff_unit_id:
                all_steps[count] = user.staff_unit.staff_division.leader.users[0].id
            else:
                staff_division = staff_division_service.get_by_id(db, user.staff_unit.staff_division.parent_group_id)
                all_steps[count] = staff_division.leader.users[0].id
            return all_steps
        staff_division = staff_division_service.get_by_id(db, user.staff_unit.staff_division_id)

        parent_id = staff_division.parent_group_id

        service_division = staff_division_service.get_by_name(db, StaffDivisionEnum.SERVICE.value)

        tmp = staff_division_service.get_by_id(db, parent_id)

        while tmp.id != service_division.id:
            tmp = staff_division_service.get_by_id(db, parent_id)
            all_steps[count] = tmp.leader.users[0].id
            parent_id = tmp.parent_group_id
            count += 1

        return all_steps
    
    
    # def remove(self, db: Session, id: str):
    #     hr_document_template = db.query(self.model).get(id)
    #     staff_unit_function.delete().where(staff_unit_function.c.staff_function_id not in(db.query(self.model).get(id)))
    #     db.delete(obj)
    #     db.flush()
    #     return obj


hr_document_template_service = HrDocumentTemplateService(HrDocumentTemplate)
