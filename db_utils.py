from sqlalchemy.orm import Session

from models import Job, LastJobId

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()

def get_last_job(db: Session):
    return db.query(Job).order_by(Job.id.desc()).first()

def create_job(db: Session, job):
    db_job = Job(
        job_id = job['job_id'],
        job_title = job['job_title'],
        company_title = job['company_title'],
        job_deadline = job['job_deadline'],
        job_salary = job['job_salary'],
        job_vacancy_number = job['job_vacancy_number'],
        job_type = job['job_type'],
        job_role = job['job_role'],
        job_gender = job['job_gender'],
        job_areas = job['job_areas'],
        job_description = job['job_description'],
        job_requirements = job['job_requirements'],
        job_benefits = job['job_benefits']
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_last_job_id(db: Session):
    return db.query(LastJobId).first()

def create_last_job_id(db: Session, last_job_id):
    db_last_job_id = LastJobId(
        last_job_id = last_job_id
    )
    db.add(db_last_job_id)
    db.commit()
    db.refresh(db_last_job_id)
    return db_last_job_id

def update_last_job_id(db: Session, id, new_last_job_id):
    db.query(LastJobId).filter(LastJobId.id == id).update({'last_job_id': new_last_job_id})
    db.commit()
    return