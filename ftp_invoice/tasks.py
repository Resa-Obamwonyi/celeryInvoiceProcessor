import requests
import os

from celery import shared_task
from datetime import datetime
from dotenv import load_dotenv
from .utils import fetch_invoice_from_ftp


load_dotenv()

URL = "https://staging.helloagain.at/external/api/v1/receipts/"
HEADERS = {"helloagain-api-key": os.environ.get("API_KEY")}

@shared_task(name='process_invoice_task')
def process_invoice_task():
    # get invoice data
    invoice_data = fetch_invoice_from_ftp()
    # invoice_data = [{'TS': '01.02.23 14:03', 'N': 'Stay 3 Nights', 'T': '234.03€', 'CID': '3454543', 'FN': 'Ben', 'LN': 'Highlander'}, {'TS': '01.02.23 14:03', 'N': 'Drinks', 'T': '34.03€', 'CID': '3454543', 'FN': 'Ben', 'LN': 'Highlander'}, {'TS': '01.02.23 14:03', 'N': 'Massage', 'T': '50 €', 'CID': '3454543', 'FN': 'Ben', 'LN': 'Highlander'}, {'TS': '03.12.22 16:00', 'N': 'Stay 1 Night', 'T': '100 €', 'CID': '923242', 'FN': 'Lisa', 'LN': 'Smith'}]
    print(invoice_data)
    if invoice_data:
        print("SENDING DATA")
        # send invoice data to api endpoint
        for indx, row in enumerate(invoice_data[0:2]):
            date_time_obj = datetime.strptime(row["TS"], '%d.%m.%y %H:%M')
            # "2023-04-21T14:11:44.059Z",

            time_and_date = date_time_obj.strftime("%Y-%m-%dT%H:%M:%S")
            data = {"customer_id": row["CID"], 
                    "receipt_nr": str(indx+100),
                    "time_and_date": time_and_date,
                    "total": float(row["T"].strip("€")),
                    "receipt_text": row["N"],
                    }
            print("TASK DATA:\n", data)
            req = requests.post(URL, data, headers=HEADERS)
            print(req.status_code, req.text)
            if req.status_code == 200 or req.status_code == 201:
                print("DONE")

process_invoice_task()