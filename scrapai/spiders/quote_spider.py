import scrapy
from scrapy.selector import Selector

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class QuoteSpider(scrapy.Spider):
    name = "quotes"
    delay = 4

    with open('urls') as urls:
        start_urls = [url for url in urls]

    def __init__(self):
        self.browser = webdriver.Firefox()

    def parse(self, response):
        self.browser.get(response.url)

        try:
            WebDriverWait(self.browser, self.delay).until(EC.presence_of_all_elements_located(
                self.browser.find_elements_by_class_name("arrow")))
            print("Page is ready!")
        except TimeoutException:
            print("Loading took too much time!")

        html = self.browser.page_source

        response = Selector(text=html)
        arrow_list = response.css('svg.arrow g').re(r'\(.*?(\d+).*\1?\)')

        filename = 'results.csv'
        with open(filename, 'w') as f:
            for arrow in arrow_list:
                f.write("{}\n".format(arrow))

        # self.browser.quit()
        self.log('Saved file {}'.format(filename))
