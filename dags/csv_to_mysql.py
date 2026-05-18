# ignore-missing-imports = ["*"]
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from airflow.providers.mysql.hooks.mysql import MySqlHook

def read_csv():
    df = pd.read_csv('/opt/airflow/data/people.csv')
    return df.to_dict('records')

def load_to_mysql(**context):
    hook = MySqlHook(mysql_conn_id='mysql_default')
    records = context['ti'].xcom_pull(task_ids='read_csv')
    df = pd.DataFrame(records)
    
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS people (
            id INT,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            age INT,
            email VARCHAR(100),
            department VARCHAR(50),
            salary INT,
            hire_date DATE,
            city VARCHAR(50),
            employment_status VARCHAR(20)
        )
    """)
    
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO people VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, tuple(row))
    
    conn.commit()
    cursor.close()
    conn.close()

with DAG(
    dag_id='csv_to_mysql',
    start_date=datetime(2024, 1, 1),
    schedule_interval="@once",
    catchup=False,
) as dag:

    task_read = PythonOperator(
        task_id = 'read_csv',
        python_callable = read_csv,
    )

    task_load = PythonOperator(
        task_id = 'load_to_mysql',
        python_callable = load_to_mysql,
        provide_context = True,
    )

    task_read >> task_load