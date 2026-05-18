# CSV to MySQL Airflow Pipeline

An end-to-end data pipeline built with Apache Airflow, MySQL, and Docker.

## What it does
Loads a 200-row employee dataset (CSV) into a MySQL database using an Airflow DAG with two tasks:
- `read_csv` — reads `people.csv` into memory
- `load_to_mysql` — creates the table and inserts all records

## Stack
- Apache Airflow 2.9.1
- MySQL 8.0
- PostgreSQL 17 (Airflow metadata DB)
- Docker Compose
- Python (pandas, pymysql, sqlalchemy)

## Setup
1. Clone the repo
2. Copy `.env.example` to `.env` and fill in values
3. Run `docker compose up airflow-init` to initialize
4. Run `docker compose up -d` to start all services
5. Open `http://localhost:8080` and log in with the credentials you set in `.env`
6. Trigger the `csv_to_mysql` DAG

## Screenshots
![DAG Success](screenshots/dag_success.png)
![MySQL Data](screenshots/mysql_data.png)