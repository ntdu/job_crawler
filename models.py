from sqlalchemy import Column, Integer, String

from database import Base

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer)
    job_title = Column(String)
    company_title = Column(String)
    job_deadline = Column(String)
    job_salary = Column(String)
    job_vacancy_number = Column(String)
    job_type = Column(String)
    job_role = Column(String)
    job_gender = Column(String)
    job_areas = Column(String)
    job_description = Column(String)
    job_requirements = Column(String)
    job_benefits = Column(String)


class LastJobId(Base):
    __tablename__ = 'lastjobid'

    id = Column(Integer, primary_key=True, index=True)
    last_job_id = Column(Integer)
    