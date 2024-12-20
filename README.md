# Python Job Scraper

This Python project is a web scraper designed to extract job listings from a job board website (Just Join IT). The scraper gathers detailed job information, including job title, company name, locat ion, salary, and required technologies, and stores the data in a PostgreSQL database using SQLAlchemy. This project also serves as a data input source for subsequent projects and can be expanded in the future to include additional job boards.


## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Database Schema](#database-schema)

## Features

- **Job Scraping**: Extracts job listings from a job board.
- **Data Storage**: Stores job listings in a PostgreSQL database using SQLAlchemy.
- **Technology Parsing**: Extracts required technologies and their proficiency levels.
- **Duplicate Check**: Ensures no duplicate job listings are stored in the database.

## Technologies Used

- **Python**: Core programming language used.
- **Playwright**: Used for browser automation and web scraping.
- **SQLAlchemy**: ORM for interacting with the PostgreSQL database.
- **PostgreSQL**: Database for storing job listings.
- **Dotenv**: Manages environment variables.

## Project Structure

**Project Root**  
├── **`main.py`**          — Main script to execute the scraping and database storage  
├── **`models.py`**       — SQLAlchemy models and database initialization logic  
├── **`scraper.py`**      — Logic for scraping job listings from the website  
├── **`.env`**               — Stores DATABASE_URL env var with a value like 
└── **`README.md`**    — Project documentation  



## Setup and Installation

### Prerequisites

- Python 3.11
- Playwright
- PostgreSQL
- A PostgreSQL user and database created for the project

### Installation

1. **Clone the repository and enter the project dir:**

   
   `git clone https://github.com/reneczka/job-scraper.git`

   `cd job-scraper` 

2. **Install the required Python packages:**

   `pip install -r requirements.txt`

   `playwright install-deps chromium`

3. **Set up the `.env` file:**

   Create a `.env` file in the root directory of the project and add your PostgreSQL database URL.
   
   You can find `.env.example` in the repository.

   Replace \`user\`, \`password\`, \`host\`, and \`dbname\` with your PostgreSQL credentials and database name.  

### Usage

1. **Run the scraper:**

   Simply execute the \`main.py\` script to start scraping and storing jobs (retry if fails in the first run):  

   `python main.py` 

   The scraper will create db tables (if they don't already exist), extract the latest job listings, check for duplicates, and store new listings in the PostgreSQL database.

2. **Accessing Data:**

   You can access the scraped data using any PostgreSQL client or directly querying the database using SQLAlchemy.

### Database Schema

The project uses SQLAlchemy to define the database schema. The schema consists of two main tables:

- **Jobs**: Stores the main job information.
- **Technologies**: Stores the technologies required for each job, linked to the \`Jobs\` table.

#### Jobs Table

| Column           | Type    | Description                          |
| ---------------- | ------- | ------------------------------------ |
| id               | Integer | Primary key, auto-increment          |
| job_name         | String  | Name of the job                      |
| company_name     | String  | Name of the company offering the job |
| job_location     | String  | Location of the job                  |
| salary           | String  | Salary offered                       |
| job_url          | String  | URL of the job listing               |
| type_of_work     | String  | Type of work (e.g., remote, onsite)  |
| experience       | String  | Required experience level            |
| employment_type  | String  | Type of employment (e.g., full-time) |
| operating_mode   | String  | Operating mode (e.g., hybrid)        |
| job_description  | Text    | Description of the job               |

#### Technologies Table

| Column  | Type    | Description               |
| ------- | ------- | ------------------------- |
| id      | Integer | Primary key, auto-increment |
| tech    | String  | Name of the technology    |
| level   | String  | Proficiency level         |
| job_id  | Integer | Foreign key to Jobs table |

