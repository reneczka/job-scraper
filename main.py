# main.py
from sqlalchemy.orm import sessionmaker
from models import Job, Technology, init_db

# Initialize database and create a session
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

# Data to be inserted
data = {
    'job_name': 'Data Management Associate',
    'company_name': 'Avenga',
    'job_location': 'Warszawa',
    'salary': '10 000 - 12 700 pln',
    'job_url': 'https://justjoin.it/offers/avenga-data-management-associate-warszawa-python',
    'type_of_work': 'Full-time',
    'experience': 'Junior',
    'employment_type': 'Permanent',
    'operating_mode': 'Remote',
    'job_description': 'Requirements:\n\nUniversity degree or equivalent (preferable in Computer Sciences, Information & Technology or similar)\n1+ year of experience in enterprise developing/modelling in one of technologies: Power BI\xa0data modelling, dashboard/visualization, Power Query, DAX formulas and data warehousing concepts/models, Power App and Power Automate design and development\n1+ year of experience with cloud-based Big Data platforms, Data Quality, Data Catalog solutions, and Data Analytics, preferably based on Microsoft Technology (e.g. Fabric/Azure Synapse Analytics, Azure Data Lake Storage, Power BI,\xa0MS Purview , Databricks, Spark, etc.).\n\xa0Knowledge of data governance practices, business, and technology issues related to the management of enterprise information assets\n\xa0Proficiency in SQL and other data manipulation languages including joins, aggregations and subqueries.\nPractical Experience with Python, R, or other data-related programming\xa0languages/libraries (e.g. PySpark, Pandas, NumPy etc.) is a plus\nFluent English\n\n\n\n\nResponsibilities:\n\n\xa0Assist in designing, implementing, and supporting data governance, data quality and master data management solutions within the organization\xa0under the guidance of senior team members\nWork with relevant teams to monitor, rectify and improve data quality\xa0\nHelp and contribute to the enhancement and maintenance of the corporate Data Catalogue, ensuring accurate metadata management and data classification.\nAssist in creating and implementing processes for data/metadata collection, storage, use, and governance in the corporate Big Data Platform\nContribute to the development of advanced data models to drive business insights and decision-making, addressing common challenges related to data silos and ensuring data consistency across all systems.\n\n\n\n\n\n',
    'technologies': [
        {'tech': 'Power BI', 'level': 'Junior'},
        {'tech': 'Spark', 'level': 'Junior'},
        {'tech': 'Databricks', 'level': 'Junior'},
        {'tech': 'SQL', 'level': 'Junior'},
        {'tech': 'Python', 'level': 'Junior'},
        {'tech': 'R', 'level': 'Nice To Have'}
    ]
}

# Create a new job entry
new_job = Job(
    job_name=data['job_name'],
    company_name=data['company_name'],
    job_location=data['job_location'],
    salary=data['salary'],
    job_url=data['job_url'],
    type_of_work=data['type_of_work'],
    experience=data['experience'],
    employment_type=data['employment_type'],
    operating_mode=data['operating_mode'],
    job_description=data['job_description']
)

# Add technologies to the job
for tech in data['technologies']:
    new_technology = Technology(tech=tech['tech'], level=tech['level'], job=new_job)
    session.add(new_technology)

# Add the job (with its technologies) to the session and commit
session.add(new_job)
session.commit()

# Query the database to verify insertion
jobs = session.query(Job).all()
for job in jobs:
    print(f"Job ID: {job.id}, Name: {job.job_name}")
    for tech in job.technologies:
        print(f"  Tech: {tech.tech}, Level: {tech.level}")
