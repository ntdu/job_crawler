from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db_utils import get_jobs, create_job, get_last_job, get_last_job_id, create_last_job_id, update_last_job_id
from crawler import topcv_crawler
from database import SessionLocal, engine
from models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
MEDIA_ROOT = 'media'

origins = [
    "http://investment-admin.jobfi.vn",
    # "http://investment-admin.jobfi.vn:3011",
    # "http://investment-admin.jobfi.vn:8080",
    "http://localhost:3011",
    "http://localhost",
    "http://localhost:8080",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def main():
    return 'Jobs Crawler'


@app.get("/jobs/")
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = get_jobs(db, skip=skip, limit=limit)
    return jobs


@app.get("/topcv_crawler_trigger/")
def topcv_crawler_trigger(db: Session = Depends(get_db)):
    last_job_id_obj = get_last_job_id(db=db)
    if not last_job_id_obj: last_job_id_obj = create_last_job_id(db=db, last_job_id=0)
       
    id, last_job_id = last_job_id_obj.id, last_job_id_obj.last_job_id

    print(id)
    print(last_job_id)

    jobs = topcv_crawler(last_job_id)
    if jobs:
        update_last_job_id(db=db, id=id, new_last_job_id=jobs[0]['job_id'])
        for job in jobs: create_job(db=db, job=job)
    return 'Done'