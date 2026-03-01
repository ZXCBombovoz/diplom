from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    owner_id = Column(Integer, nullable=False)
    secret_flag = Column(String, nullable=True)
    
class LtiUser(Base):
    __tablename__ = "lti_users"

    id = Column(Integer, primary_key=True)
    lti_user_id = Column(String, unique=True)
    local_user_id = Column(Integer)

