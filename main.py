# main.py
from sqlalchemy.orm import sessionmaker
from models import Job, Technology, init_db
from scraper import scrape_jobs

# Initialize database and create a session
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

scraped_jobs = scrape_jobs()

for job in scraped_jobs:
    existing_job = session.query(Job).filter_by(job_url=job['job_url']).first()
    if existing_job is None:
        new_job = Job(job_name=job['job_name'],
                    company_name=job['company_name'],
                    job_location=job['job_location'],
                    salary=job['salary'],
                    job_url=job['job_url'],
                    type_of_work=job['type_of_work'],
                    experience=job['experience'],
                    employment_type=job['employment_type'],
                    operating_mode=job['operating_mode'],
                    job_description=job['job_description'])

        session.add(new_job)

        for tech in job['technologies']:
            new_technology = Technology(tech=tech['tech'], level=tech['level'], job=new_job)

            session.add(new_technology)
        print(f"Job added to database")
    else:
        print(f"Job already exists in the database: {job['job_url']}")


session.commit()