from sqlalchemy import Column, String, Boolean, Date
from webpage.data.modelbase import SqlAlchemyBase
import datetime
import uuid


class Account(SqlAlchemyBase):
    __tablename__ = 'Account'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()).replace('-',''))

    password_hash = Column(String)
    created = Column(Date, default=datetime.datetime.now)
    email_confirmed = Column(Boolean, nullable=False, default=False)
    is_super_user = Column(Boolean, nullable=False, default=False)
    email = Column(String, nullable=False, index=True, unique=True)