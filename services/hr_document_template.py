import uuid
import json

from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List, Union, Dict

from exceptions import NotFoundException
from models import (
    HrDocumentTemplate,
    HrDocumentStep,
    DocumentStaffFunction,
    User,
    HrDocumentTemplateEnum,
    StaffDivisionEnum,
    StaffUnit,
)

from schemas import (
    HrDocumentTemplateCreate,
    HrDocumentTemplateUpdate,
    HrDocumentTemplateRead,
    DocumentStaffFunctionCreate,
    HrDocumentStepCreate,
    SuggestCorrections,
    NotificationCreate,
    DocumentStaffFunctionAppendToStaffUnit,
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


class HrDocumentTemplateService(
    ServiceBase[HrDocumentTemplate,
                HrDocumentTemplateCreate,
                HrDocumentTemplateUpdate]
):  
    def create_template(
        self, db: Session, body: HrDocumentTemplateCreate, role: str
    ) -> HrDocumentTemplateRead:
        current_user_staff_unit_id = db.query(StaffUnit).filter(StaffUnit.id == role).first()

        obj_in_data = jsonable_encoder(body)
        hr_document_template = self.model(**obj_in_data)
        if isinstance(hr_document_template.properties, dict):
            hr_document_template.properties = json.dumps(hr_document_template.properties)
        if isinstance(hr_document_template.actions, dict):
            hr_document_template.actions= json.dumps(hr_document_template.actions)
        if isinstance(hr_document_template.description, dict):
            hr_document_template.description= json.dumps(hr_document_template.description)
        hr_document_template.maintainer_id = current_user_staff_unit_id.id
        hr_document_template.is_draft = False
        db.add(hr_document_template)
        db.commit()
        if isinstance(hr_document_template.properties, str):
            hr_document_template.properties = json.loads(hr_document_template.properties)
        if isinstance(hr_document_template.actions, str):
            hr_document_template.actions= json.loads(hr_document_template.actions)
        if isinstance(hr_document_template.description, str):
            hr_document_template.description= json.loads(hr_document_template.description)
        return hr_document_template
    
    def create_template_draft(
        self, db: Session, body: HrDocumentTemplateCreate, role: str
    ) -> HrDocumentTemplateRead:
        current_user_staff_unit_id = staff_unit_service.get_by_id(db, role)

        obj_in_data = jsonable_encoder(body)
        hr_document_template = self.model(**obj_in_data)
        if isinstance(hr_document_template.properties, dict):
            hr_document_template.properties = json.dumps(hr_document_template.properties)
        if isinstance(hr_document_template.actions, dict):
            hr_document_template.actions= json.dumps(hr_document_template.actions)
        if isinstance(hr_document_template.description, dict):
            hr_document_template.description= json.dumps(hr_document_template.description)
        hr_document_template.maintainer_id = current_user_staff_unit_id.id
        hr_document_template.is_draft = False

        hr_document_template.maintainer_id = current_user_staff_unit_id.id
        hr_document_template.is_draft = True
        db.add(hr_document_template)
        db.commit()
        if isinstance(hr_document_template.properties, str):
            hr_document_template.properties = json.loads(hr_document_template.properties)
        if isinstance(hr_document_template.actions, str):
            hr_document_template.actions= json.loads(hr_document_template.actions)
        if isinstance(hr_document_template.description, str):
            hr_document_template.description= json.loads(hr_document_template.description)

        return hr_document_template
    
    def update(
        self,
        db: Session,
        *,
        hr_document_template: HrDocumentTemplate,
        obj_in: HrDocumentTemplateUpdate
    ) -> HrDocumentTemplate:
        obj_data = jsonable_encoder(hr_document_template)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(hr_document_template, field, update_data[field])
        if isinstance(hr_document_template.properties, dict):
            hr_document_template.properties = json.dumps(hr_document_template.properties)
        if isinstance(hr_document_template.actions, dict):
            hr_document_template.actions= json.dumps(hr_document_template.actions)
        if isinstance(hr_document_template.description, dict):
            hr_document_template.description= json.dumps(hr_document_template.description)
        hr_document_template.is_draft = False
        db.add(hr_document_template)
        db.commit()
        if isinstance(hr_document_template.properties, str):
            hr_document_template.properties = json.loads(hr_document_template.properties)
        if isinstance(hr_document_template.actions, str):
            hr_document_template.actions= json.loads(hr_document_template.actions)
        if isinstance(hr_document_template.description, str):
            hr_document_template.description= json.loads(hr_document_template.description)
        return hr_document_template
    

    def get_by_id(self, db: Session, id: str) -> HrDocumentTemplate:
        hr_document_template = super().get(db, str(id))
        if hr_document_template is None:
            raise NotFoundException(
                detail=f"HrDocumentTemplate with id: {id} is not found!"
            )
        if isinstance(hr_document_template.properties, str):
            hr_document_template.properties = json.loads(hr_document_template.properties)
        if isinstance(hr_document_template.description, str):
            hr_document_template.description = json.loads(hr_document_template.description)
        if isinstance(hr_document_template.actions, str):
            hr_document_template.actions = json.loads(hr_document_template.actions)
        return hr_document_template

    def get_steps_by_document_template_id(
        self, db: Session, document_template_id: str, user_id: str
    ) -> dict[str, Union[Union[str, Dict[int, str]], list[str]]]:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise NotFoundException(
                detail=f"User with id: {user_id} is not found!")

        initial_step = hr_document_step_service.get_initial_step_for_template(
            db, document_template_id
        )

        all_steps = hr_document_step_service.get_all_by_document_template_id(
            db, document_template_id
        )

        all_functions = (
            db.query(DocumentStaffFunction)
            .filter(
                HrDocumentStep.hr_document_template_id == document_template_id,
                DocumentStaffFunction.priority != 1,
            )
            .join(HrDocumentStep.staff_function)
            .order_by(DocumentStaffFunction.priority.asc())
            .all()
        )

        all_steps.remove(initial_step)

        steps = {}
        for function, step in zip(all_functions, all_steps):
            function: DocumentStaffFunction

            if step.is_direct_supervisor is not None:
                steps[str(function.priority)] = self.get_all_supervisors(
                    db, step.id, step.is_direct_supervisor, document_template_id, user_id
                )
                continue
            if step.category is not None:
                category: BaseCategory = categories.get(step.category, None)
                if category is None:
                    raise NotFoundException(
                        detail=f"Category with id: {step.category} is not found!"
                    )
                steps[str(function.priority)] = category.handle(db, str(user_id))
                continue
            staff_units_ids = [unit.id for unit in function.staff_units]
            user = (
                db.query(User).filter(
                    User.staff_unit_id.in_(staff_units_ids)).first()
            )
            steps[str(function.priority)] = str(user.id)
        return steps

    def get_all_by_name(self, db: Session, name: str, skip: int, limit: int):
        if name:
            hr_document_templates = (
                db.query(HrDocumentTemplate)
                .filter(
                    HrDocumentTemplate.is_active == True,
                    (
                        HrDocumentTemplate.name.ilike(f"%{name}%")
                        | HrDocumentTemplate.description.ilike(f"%{name}%")
                    ),
                    HrDocumentTemplate.is_draft == False
                )
                .filter(HrDocumentTemplate.is_visible == True)
                .filter(HrDocumentTemplate.is_draft == False)
                .order(HrDocumentTemplate.created_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )
            
            for template in hr_document_templates:
                if isinstance(template.properties, str):
                    template.properties = json.loads(template.properties)
                if isinstance(template.description , str):
                    template.description = json.loads(template.description)
                if isinstance(template.actions , str):
                    template.actions = json.loads(template.actions)
            
            return hr_document_templates
        return self.get_all_active(db, skip, limit)
    

    def get_all_active(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[HrDocumentTemplateRead]:
        hr_document_templates = (
            db.query(HrDocumentTemplate)
            .filter(HrDocumentTemplate.is_active == True)
            .filter(HrDocumentTemplate.is_visible == True)
            .filter(HrDocumentTemplate.is_draft == False)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        count = (
            db.query(HrDocumentTemplate)
            .filter(HrDocumentTemplate.is_active == True)
            .filter(HrDocumentTemplate.is_visible == True)
            .filter(HrDocumentTemplate.is_draft == False)
            .count()
        )
        for template in hr_document_templates:
            if isinstance(template.properties, str):
                template.properties = json.loads(template.properties)
            if isinstance(template.description , str):
                template.description = json.loads(template.description)
            if isinstance(template.actions , str):
                template.actions = json.loads(template.actions)
        return {"total": count, "objects": hr_document_templates}
        
    def get_all_drafts(
        self, db: Session, name: str, skip: int = 0, limit: int = 100
    ) -> List[HrDocumentTemplateRead]:
        if name:
            hr_document_templates = (
                db.query(HrDocumentTemplate)
                .filter(
                    HrDocumentTemplate.is_active == True,
                    (
                        HrDocumentTemplate.name.ilike(f"%{name}%")
                        | HrDocumentTemplate.description.ilike(f"%{name}%")
                    ),
                    HrDocumentTemplate.is_draft == False
                )
                .filter(HrDocumentTemplate.is_visible == True)
                .filter(HrDocumentTemplate.is_draft == True)
                .offset(skip)
                .limit(limit)
                .all()
            )
            count = (
                db.query(HrDocumentTemplate)
                .filter(
                    HrDocumentTemplate.is_active == True,
                    (
                        HrDocumentTemplate.name.ilike(f"%{name}%")
                        | HrDocumentTemplate.description.ilike(f"%{name}%")
                    ),
                    HrDocumentTemplate.is_draft == False
                )
                .filter(HrDocumentTemplate.is_visible == True)
                .filter(HrDocumentTemplate.is_draft == True)
                .count()
            )
            for template in hr_document_templates:
                if isinstance(template.properties, str):
                    template.properties = json.loads(template.properties)
                if isinstance(template.description , str):
                    template.description = json.loads(template.description)
                if isinstance(template.actions , str):
                    template.actions = json.loads(template.actions)
            return hr_document_templates
        else:
            hr_document_templates = (
                db.query(HrDocumentTemplate)
                .filter(HrDocumentTemplate.is_draft == True)
                .filter(HrDocumentTemplate.is_visible == True)
                .offset(skip)
                .limit(limit)
                .all()
            )
            
            count = (
                db.query(HrDocumentTemplate)
                .filter(HrDocumentTemplate.is_draft == True)
                .filter(HrDocumentTemplate.is_visible == True)
                .count()
            )
            for template in hr_document_templates:
                template.properties = json.loads(template.properties)
                template.description = json.loads(template.description)
                template.actions = json.loads(template.actions)
            return {"total": count, "objects": hr_document_templates}

    def get_all_archived(self, db: Session, skip: int, limit: int):
        hr_document_templates = (
            db.query(self.model)
            .filter(self.model.is_active == False)
            .filter(self.model.is_visible == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        
        count = (
            db.query(self.model)
            .filter(self.model.is_active == False)
            .filter(self.model.is_visible == True)
            .count()
        )
        for template in hr_document_templates:
            if isinstance(template.properties, str):
                template.properties = json.loads(template.properties)
            if isinstance(template.description , str):
                template.description = json.loads(template.description)
            if isinstance(template.actions , str):
                template.actions = json.loads(template.actions)
        return {"total": count, "objects": hr_document_templates}

    def duplicate(self, db: Session, id: str):
        template = super().get_by_id(db, str(id))
        new_template = self.create(
            db,
            {
                "name": (template.name
                if template.name is None
                else template.name + " (Копия)"),
                "nameKZ": template.nameKZ + " (Копия)",
                "path": template.path,
                "pathKZ": template.pathKZ,
                "subject_type": template.subject_type,
                "properties": template.properties,
                "description": template.description,
                "actions": template.actions,
                "is_visible": template.is_visible,
                "is_draft": template.is_draft
            }
        )
        steps = hr_document_step_service.get_all_by_document_template_id(
            db, template.id
        )
        for step in steps:
            staff_function: DocumentStaffFunction = step.staff_function
            new_staff_function = document_staff_function_service.create(
                db,
                DocumentStaffFunctionCreate(
                    name=staff_function.name + " (Копия)",
                    nameKZ=staff_function.nameKZ
                    if staff_function.nameKZ is None
                    else staff_function.nameKZ + " (Копия)",
                    hours_per_week=staff_function.hours_per_week,
                    priority=staff_function.priority,
                    role_id=staff_function.role_id,
                    jurisdiction_id=staff_function.jurisdiction_id,
                ),
            )
            new_staff_function.staff_units = staff_function.staff_units
            hr_document_step_service.create(
                db,
                HrDocumentStepCreate(
                    hr_document_template_id=new_template.id,
                    staff_function_id=new_staff_function.id,
                    is_direct_supervisor=step.is_direct_supervisor,
                    category=step.category,
                ),
            )
            document_staff_function_service.append_to_staff_unit(
                db,
                DocumentStaffFunctionAppendToStaffUnit(
                    staff_function_id=new_staff_function.id,
                    staff_unit_ids=[i.id for i in staff_function.staff_units]
                )
            )
            db.add(new_staff_function)
        db.add(new_template)
        db.commit()
        if isinstance(new_template.properties, str):
            new_template.properties = json.loads(new_template.properties)
        if isinstance(new_template.actions, str):
            new_template.actions= json.loads(new_template.actions)
        if isinstance(new_template.description, str):
            new_template.description= json.loads(new_template.description)
        return new_template

    async def suggest_corrections(
        self, db: Session, body: SuggestCorrections, current_user_id: str
    ):
        template = self.get_by_id(db, body.hr_document_template_id)
        for i in template.maintainer.actual_users:
            db.add(
                notification_service.create(
                    db,
                    NotificationCreate(
                        message=template.name + body.text,
                        sender_id=current_user_id,
                        receiver_id=i.id,
                    ),
                )
            )
            await notification_manager.broadcast(body.text, i.id)

    def get_staff_list(self, db: Session):
        res = (
            db.query(self.model)
            .filter(self.model.name == HrDocumentTemplateEnum.STAFF_LIST.value)
            .first()
        )
        if res is None:
            raise NotFoundException(
                detail=("HrDocumentTemplate with name: "
                        f"{HrDocumentTemplateEnum.STAFF_LIST.value} is not found!")
            )
        return res

    def get_disposition(self, db: Session):
        res = (
            db.query(self.model)
            .filter(self.model.name == HrDocumentTemplateEnum.DISPOSITION.value)
            .first()
        )
        if res is None:
            raise NotFoundException(
                detail=("HrDocumentTemplate with name: "
                        f"{HrDocumentTemplateEnum.DISPOSITION.value} is not found!")
            )
        return res

    def get_staff_unit(self, db: Session):
        res = (
            db.query(self.model)
            .filter(self.model.name == HrDocumentTemplateEnum.STAFF_UNIT.value)
            .first()
        )
        if res is None:
            raise NotFoundException(
                detail=("HrDocumentTemplate with name: "
                        f"{HrDocumentTemplateEnum.STAFF_UNIT.value} is not found!")
            )
        return res

    def get_all(self, db: Session, ids: List[str]):
        return self._get_all(db, ids).all()

    def get_all_skip(self, db: Session,
                     ids: List[str], skip: int, limit: int):\
                         
        hr_document_templates = self._get_all(db, ids).offset(skip).limit(limit).all()
        for hr_document_template in hr_document_templates:
            hr_document_template.description = json.loads(hr_document_template.description)
            hr_document_template.actions = json.loads(hr_document_template.actions)
            hr_document_template.properties = json.loads(hr_document_template.properties)
        return hr_document_templates

    def _get_all(self, db: Session, ids: List[str]):
        return (
            db.query(self.model)
            .filter(
                self.model.id.in_(ids),
                self.model.is_active == True,
                self.model.is_visible == True,
            )
        )

    def get_all_supervisors(
        self,
        db: Session,
        step_id: str,
        is_direct: bool,
        template_id: str,
        user_id: str,
    ):
        user = db.query(User).filter(User.id == user_id).first()
        count = 0
        #all_steps = {}
        all_steps = []
        
        if user.staff_unit.staff_division.leader_id != user.staff_unit_id:
            #TODO: add exception if leader id does not exist
            leader_id = user.staff_unit.staff_division.leader_id
            leader = db.query(User).filter(User.staff_unit_id == leader_id).first()
            #all_steps[count] = leader.id 
            all_steps.append(leader.id)
        else:
            if user.staff_unit.staff_division.leader_id is None:
                raise NotFoundException(
                    detail="Leader for staff division of this user is not found!"
                )
            parent_id = user.staff_unit.staff_division.parent_group_id
            if parent_id:
                leader_id = staff_division_service.get_by_id(db, parent_id).leader_id
                leader = db.query(User).filter(User.staff_unit_id == leader_id).first()
                #all_steps[count] = leader.id
                all_steps.append(leader.id)
                
        if is_direct:
            if user.staff_unit.staff_division.leader_id is None:
                raise NotFoundException(
                        detail="Direct Leader for staff division of this user is not found!"
                    )
            return all_steps

        service_division = staff_division_service.get_by_name(
            db, StaffDivisionEnum.SERVICE.value
        )
        if service_division.id == user.staff_unit.staff_division.id:
            #all_steps[count] = user.staff_unit.staff_division.leader.users[0].id
            all_steps.append(leader.id)
            return all_steps

        parent_id = user.staff_unit.staff_division.parent_group_id
        
        if parent_id is not None:
            tmp = user.staff_unit.staff_division

            while tmp.parent_group_id != service_division.id:
                tmp = staff_division_service.get_by_id(db, tmp.parent_group_id)
                if tmp.leader is None:
                    continue
                all_steps.append(tmp.leader.users[0].id)
                #all_steps[count] = tmp.leader.users[0].id
                count += 1

        return all_steps


hr_document_template_service = HrDocumentTemplateService(HrDocumentTemplate)
