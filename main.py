import argparse
import math
import os
from sodapy import Socrata
from datetime import datetime
from elasticsearch import Elasticsearch

parser = argparse.ArgumentParser()
parser.add_argument('--page_size', type=int,
                    help='how many rows to get per page', required=True)
parser.add_argument('--num_pages',type=int,
                    help='how many pages to get in total')
args = parser.parse_args()

DATASET_ID = os.environ["DATASET_ID"]
APP_TOKEN = os.environ["APP_TOKEN"]
ES_HOST = os.environ["ES_HOST"]
ES_USERNAME = os.environ["ES_USERNAME"]
ES_PASSWORD = os.environ["ES_PASSWORD"]


client = Socrata("data.cityofnewyork.us", APP_TOKEN ,timeout=50000)
number_of_rows=int(client.get(DATASET_ID, select='COUNT(*)')[0]['COUNT'])

if args.num_pages == 0:
    args.num_pages= math.ceil(number_of_rows/args.page_size)
else:
    args.num_pages= args.num_pages


if __name__ == '__main__':
    try:
        es = Elasticsearch(ES_HOST,http_auth=(ES_USERNAME,ES_PASSWORD))
        es.indices.create(index='nycparking')
        
    except Exception: 
        print("Index already exists! Skipping")
    
    for page in range(0,args.num_pages):
        offset= page* args.page_size
        results = client.get(DATASET_ID,limit=args.page_size, offset=offset)
        for result in results:
            try:
                result["issue_date"] = str(result["issue_date"])
                result["issue_date"] = datetime.strptime(result["issue_date"],"%m/%d/%Y").date()
                result["precinct"] = int(result["precinct"])
                result["fine_amount"] = float(result["fine_amount"])
                result["reduction_amount"] = float(result["reduction_amount"])
            except Exception as e:
                print(f"Error!: {e}, skipping row: {result}")
                continue
            try:   
                es.index(index='nycparking',doc_type='parking', body=result)
            except Exception as e:
                print(f"Failed to insert in ES: {e}, skipping row: {result}")
                continue
        

