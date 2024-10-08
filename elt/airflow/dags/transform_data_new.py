from airflow.decorators import dag, task
from pendulum import datetime
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine

@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    tags=["transform"],
    catchup=False,
)
def transform_data_new():
    @task
    def get_db_connection_params():
        # Return the connection parameters as a dictionary (JSON serializable)
        return {
            'extract_url': 'postgresql+psycopg2://postgres:admin@host.docker.internal:5433/metrodata',
            'loading_url':'postgresql+psycopg2://postgres:admin@host.docker.internal:5433/metrodata_prod'
        }
    
    @task
    def transform_stock_price(db_params):
        # Recreate the staging area engine inside the task
        extract_engine = create_engine(db_params['extract_url'])
        
        # Get data from PostgreSQL
        table_sql_transform = pd.read_sql(
            sql='''
            SELECT *, (sp."High" - sp."Low") as "Price Range" 
            FROM stock_price sp 
            WHERE 1=1;
            ''', 
            con=extract_engine
        )
        
        # Recreate the data warehouse engine inside the task
        loading_engine = create_engine(db_params['loading_url'])
                
        # Load data after transformation to PostgreSQL
        TABLE_NAME = 'aggregate_stock_price'
        table_sql_transform.to_sql(name=TABLE_NAME, con=loading_engine, index=False, if_exists='replace')
    
    @task.bash
    def success():
        return 'echo "The DAG is running well"'
    
    # Call the tasks
    transform_stock_price(get_db_connection_params()) >> success()

transform_data_new()