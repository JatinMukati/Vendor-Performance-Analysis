import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
    )

engine= create_engine ('postgresql://postgres:1234@localhost:5432/vendors_project')

def load_raw_data():
    '''this fuction will load the CSVs as dataframe and ingest into db'''
    start = time.time()
    for file in os.listdir('data'):
        if '.csv' in file:
            df=pd.read_csv('data/'+file)
            logging.info(f'Ingesting {file} in db')
            table_name = file[:-4]  # Remove .csv extension
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            
    end = time.time()
    total_time = (end - start)/60
    logging.info('----------------Ingestion Complete-------------')
    logging.info(f'\nTotal Time Taken: {total_time} minutes')

if __name__ =='__main__':
    load_raw_data()