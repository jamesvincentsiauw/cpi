from adapter.cpi import CPIScraper
from adapter.rabbitmq import RabbitPublisher
import json

def main(thread: int, publisher: RabbitPublisher):
    # Instantiate CPI Scraper
    cpi = CPIScraper()
    cpi_result = cpi.run()

    # Process CPI Data and Publish Data
    if cpi_result:
        cpi_result['thread_number'] = thread
        publisher.publish_message(json.dumps(cpi_result))

if __name__ == '__main__':
    main()
