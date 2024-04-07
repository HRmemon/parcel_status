import os
import logging
import requests
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


def lambda_handler(event, context):
    try: 
        logger.info("Received event: " + str(event))
        parcel = get_parcel()
        logger.info("Parcel: " + str(parcel))
    except Exception as e:
        logger.error("Error getting parcel: " + str(e))
        raise e


# if __name__ == '__main__':
#     logging.basicConfig()
#     lambda_handler(None, None)