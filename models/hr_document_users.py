from sqlalchemy import Column, String, CHAR, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class HrDocumentUsers(Base):
    __tablename__ = 'HR_ERP_HR_DOCUMENT_USERS'

    document_id = Column(String(36), ForeignKey('SYSTEM.HR_ERP_HR_DOCUMENTS.ID'), primary_key=True)
    subject_id= Column(String(36), ForeignKey('SYSTEM.HR_ERP_USERS.ID'), primary_key=True)


    document = relationship('Document', back_populates='document_users')
    user = relationship('User', back_populates='document_users')