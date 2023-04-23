import ftplib
import os
from dotenv import load_dotenv
from csv import DictReader

load_dotenv()

# makeshift ftp server
FTP_HOSTNAME = os.environ.get('FTP_HOSTNAME')
FTP_USERNAME = os.environ.get('FTP_USERNAME')
FTP_PASSWORD = os.environ.get('FTP_PASSWORD')

# Connect FTP Server
ftp_server = ftplib.FTP(FTP_HOSTNAME, FTP_USERNAME, FTP_PASSWORD)
ftp_server.encoding = "utf-8"

# Send dummy invoice to an ftp server, for test purposes
def send_invoice_to_ftp():
    filename = "invoices_230201.csv"
    with open(filename, "rb") as file:
        ftp_server.storbinary(f"STOR {filename}", file)
        print("invoice uploaded!!")
    
    
def fetch_invoice_from_ftp():
    send_invoice_to_ftp()
    
    filename = "invoices_230201.csv"
    with open(filename, "wb") as file:
        ftp_server.retrbinary(f"RETR {filename}", file.write)
    
    invoice_content = []
    # open file in read mode
    with open(filename, 'r') as file:
        csv_dict_reader = DictReader(file, delimiter=";")
        for row in csv_dict_reader:
            invoice_content.append(row)
        print("Invoiced data all saved!!")
            
    # Close the Connection
    ftp_server.quit()
    
    return invoice_content
