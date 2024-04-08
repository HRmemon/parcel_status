import os
import logging
from urllib import response
import requests
import boto3
from bs4 import BeautifulSoup

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_parcel():
    try:
        url = 'https://mulphilog.com/tracking/556649310017966'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        shipment_div = soup.find('div', {'class': 'shipment'})
        parcel = shipment_div.find('table')
        rows = parcel.find_all('tr')

        return [ {
            'date': row.find_all('td')[0].text,
            'details': row.find_all('td')[1].text,
            'location': row.find_all('td')[2].text,
            'status': row.find_all('td')[3].text
        } for row in rows[1:]]
    except Exception as e:
        logger.error("Error getting parcel: " + str(e))
        raise e

def send_email(rows):
    ses = boto3.client('ses', region_name='ap-south-1')
    SENDER = "awsforhassan@gmail.com"
    RECIPIENT = "awsforhassan@gmail.com"
    SUBJECT = f"Parcel Status :-> {len(rows)} Updates"
    BODY_TEXT = ("Parcel Status\n\n" + "\n".join([f"{row['date']} - {row['details']} - {row['location']} - {row['status']}" for row in rows]))
    CHARSET = "UTF-8"

    try:
        # Pronvide the contents of the email.
        response = ses.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data': 'From: ' + SENDER + '\n' +
                        'To: ' + RECIPIENT + '\n' +
                        'Subject: ' + SUBJECT + '\n' +
                        'MIME-Version: 1.0\n' +
                        'Content-type: text/plain; charset=UTF-8\n' +
                        '\n' +
                        BODY_TEXT
            }
        )
        logger.info("Email sent: " + str(response))
    except Exception as e:
        logger.error("Error sending email: " + str(e))
        raise e



def lambda_handler(event, context):
    try: 
        logger.info("Received event: " + str(event))
        parcel = get_parcel()
        logger.info("Parcel: " + str(parcel))
        send_email(parcel)
    except Exception as e:
        logger.error("Error getting parcel: " + str(e))
        raise e


if __name__ == '__main__':
    logging.basicConfig()
    lambda_handler(None, None)