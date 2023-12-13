from typing import Any, Optional
import scrapy
from aerospaceproject.items import AerospaceprojectItem
from scrapy.exporters import CsvItemExporter

class Launches(scrapy.Spider):
    name = 'launches_scrape'
    def __init__(self):
        
        self.start_page = 1

    def start_requests(self):
        url = f'https://spacelaunchnow.me/launch/?page={self.start_page}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        csv_exporter = CsvItemExporter(open('launches.csv', 'ab'), delimiter=',')
        csv_exporter.start_exporting()
        for launch in response.css('tbody tr'):
            
            item = AerospaceprojectItem()
            item['name'] = launch.css('td:nth-child(1) a::text').get()
            item['status'] = launch.css('td:nth-child(2)::text').get()
            item['launch_service_provider'] = launch.css('td:nth-child(3)::text').get()
            item['rocket'] = launch.css('td:nth-child(4)::text').get()
            item['mission'] = launch.css('td:nth-child(5)::text').get()
            item['net'] = launch.css('td:nth-child(6)::text').get()
            item['pad'] = launch.css('td:nth-child(7)::text').get()

            yield item
            csv_exporter.export_item(item)
        
        csv_exporter.finish_exporting()
        next_page = f'https://spacelaunchnow.me/launch/?page={self.start_page + 1}'
        self.start_page += 1

        yield scrapy.Request(url=next_page, callback=self.parse)