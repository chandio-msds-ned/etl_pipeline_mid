import json
import pandas as pd
from pymongo import MongoClient

def load_config(path='config/db_config.json'):
    with open(path, 'r') as file:
        return json.load(file)

def load_csv_to_mongodb(csv_file, db_name, collection_name, mongo_uri):
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    df = pd.read_csv(csv_file)
    records = df.to_dict(orient='records')

    if records:
        collection.insert_many(records)
        print(f"Inserted {len(records)} records into {db_name}.{collection_name}")
    else:
        print("No data to insert.")

if __name__ == "__main__":
    config = load_config()
    load_csv_to_mongodb(
        csv_file='output/xlsx_data.csv',
        db_name='etl_weather_db',
        collection_name='etl_weather_col',
        mongo_uri=config['mongo_uri']
    )