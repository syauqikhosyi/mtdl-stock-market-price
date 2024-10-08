from airflow.decorators import dag, task
from pendulum import datetime
import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
import psycopg2

@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    tags=["extract"],
    catchup=False,
)
def extract_load_data():
    @task
    def extract_stock_price():
        mtdl = yf.Ticker("MTDL.JK")  # Download the dataset
        df = mtdl.history(start="2014-01-01", end=None)  # Get historical market data
        
        # Remove timezone information from the 'Date' index
        df.index = df.index.tz_localize(None)
        
        # Convert index to columns
        df = df.reset_index()
                
        return df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]  # Select certain columns

    @task
    def load_stock_price(df):
        # Instead of returning engine from a separate task, create the connection here
        # Connection to local postgres
        #f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}'
        db_url = 'postgresql+psycopg2://postgres:admin@host.docker.internal:5433/metrodata'
        engine = create_engine(db_url)
                
        # Load data after extraction to PostgreSQL
        TABLE_NAME = 'stock_price'
        df.to_sql(name=TABLE_NAME, con=engine, index=False, if_exists='replace')
    
    # welcome() >> load_stock_price(extract_stock_price()) >> end_task() 
    stock_data = extract_stock_price()
    load_stock_price(stock_data)

extract_load_data()