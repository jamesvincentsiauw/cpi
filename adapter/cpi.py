from lxml import html
import utils
from dotenv import load_dotenv
from logzero import logger
import datetime
import requests
import os
load_dotenv()

class CPIScraper:
    def __init__(self):
        logger.info('instantiate cpi scraper')
        self._url = os.environ.get('CPI_URL')
        self._xpath = os.environ.get('CPI_XPATH')
    
    def send_request(self):
        """
        Send request to get CPI's website HTML
        """
        return requests.get(self._url)
    
    def parse_elemets(self, html_content) -> list:
        """
        Get all CPI needed elements including month and year
        """
        tree = html.fromstring(html_content)
        return utils.get_xpath_value(tree, self._xpath, True)

    def verify_data(self, data: list) -> bool:
        """
        Verify and make sure the data is updated or not
        """
        now = datetime.datetime.now()
        month = now.strftime("%b")
        year = now.year

        if len(data) != 3 or month.lower() != data[1] or year != data[2]:
            return False
        if '%' not in data[0]:
            return False

        return True

    def run(self):
        """
        Main function to scrape CPI
        """
        try:
            logger.info('starting to scrape cpi')
            res = self.send_request()
            if res.status_code != 200:
                logger.error('status code is not 200')
                return None

            parsed_data = self.parse_elemets(res.content)
            # if not self.verify_data(parsed_data):
            #     logger.error(f'data verification failed: {parsed_data}')
            #     return None
            
            logger.info(f'cpi data for {parsed_data[1]} {parsed_data[2]}: {parsed_data[0]}')
            return {
                'cpi_data': parsed_data[0],
                'last_updated': f'{parsed_data[1]} {parsed_data[2]}',
                'scraped_at': datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            }
        except Exception as e:
            logger.exception(f'error occurs when scraping cpi: {e}')
            return None
