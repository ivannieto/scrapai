import scrapy

from selenium import webdriver
from scrapy.selector import Selector


class QuoteSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://windguru.cz/1066/',
    ]

    def __init__(self):
        self.browser = webdriver.Firefox()

    def parse(self, response):
        self.browser.get(response.url)
        html = self.browser.page_source
        response = Selector(text=html)
        arrow_list = response.css('svg.arrow g::transform::text').extract()
        filename = 'results.html'
        with open(filename, 'w') as f:
            for arrow in arrow_list:
                f.write(arrow)

        self.browser.close()
        self.log('Saved file {}'.format(filename))
