from sqlalchemy import Column, String, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HrDocumentUsers(Base):
    __tablename__ = 'hr_erp_hr_document_users'

    document_id = Column(String(36), ForeignKey('hr_erp_hr_documents.id'), primary_key=True)
    subject_id= Column(String(36), ForeignKey('hr_erp_users.id'), primary_key=True)


    # document = relationship('HrDocument', back_populates='hr_document_users')
    # user = relationship('User', back_populates='hr_document_users')