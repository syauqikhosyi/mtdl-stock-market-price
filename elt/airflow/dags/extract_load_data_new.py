from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from pendulum import datetime
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
import psycopg2

default_args = {
    "owner": "Syauqi Khosyi",
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

def extract_stock_price(ti):
    mtdl = yf.Ticker("MTDL.JK")  # Download the dataset
    df = mtdl.history(start="2014-01-01", end=None)  # Get historical market data
        
    # Remove timezone information from the 'Date' index
    df.index = df.index.tz_localize(None)
        
    # Convert index to columns
    df = df.reset_index()

    # Push the dataframe to XCom
    ti.xcom_push(key='stock_data', value=df.to_json())  # Store dataframe as JSON

    return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]  # Select certain columns

def load_stock_price(ti):
    # Pull the dataframe from XCom
    df_json = ti.xcom_pull(key='stock_data')
    df = pd.read_json(df_json)

    # Connection to local postgres
    db_url = 'postgresql+psycopg2://postgres:admin@host.docker.internal:5433/metrodata'
    engine = create_engine(db_url)
                
    # Load data after extraction to PostgreSQL
    TABLE_NAME = 'stock_price'
    df.to_sql(name=TABLE_NAME, con=engine, index=False, if_exists='replace')

with DAG(dag_id='extract_load_data_new',
         default_args=default_args,
         schedule_interval="@daily",
         tags=['extract'],
         catchup=False,
         description="Fetch Metrodata's stocks data from yfinance library"
         ) as dag:

    extract_stock_price_task = PythonOperator(
        task_id='extract_stock_price',
        python_callable=extract_stock_price,
        provide_context=True  # Allows XCom to pass data between tasks
    )

    load_stock_price_task = PythonOperator(
        task_id='load_stock_price',
        python_callable=load_stock_price,
        provide_context=True  # Enables pulling data from XCom
    )

    # Define task dependencies
    extract_stock_price_task >> load_stock_price_task
