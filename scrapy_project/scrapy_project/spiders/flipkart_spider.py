import json

import scrapy
from scrapy_project.items import FlipkartScraperItem

pages_processed = 0


class FlipkartSpider(scrapy.Spider):
    """spider class for scrape data from flipkart"""

    name = "flipkart"
    url = "https://www.flipkart.com/"
    base_url = "https://www.flipkart.com{}"
    allowed_domain = "https://www.flipkart.com/"

    def __init__(self, pages='', **kwargs):
        self.pages = int(pages) if pages else 9999
        super(FlipkartSpider, self).__init__(**kwargs)

    def start_requests(self):
        """method to start scrapy request"""

        urls = ['https://www.flipkart.com/', ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_main_category)

    def parse_main_category(self, response):
        """method for parse all main categories"""

        main_categories = response.css('div[class="eFQ30H"] a::attr(href)').getall()
        if main_categories:
            for category in main_categories:
                if category and 'mobile-phones' in category:
                    yield scrapy.Request(url=category, callback=self.parse_mobile_brands)

    def parse_mobile_brands(self, response):
        """method for get all brand url for mobile category"""
        global pages_processed
        brand_urls = response.css('a::attr(href)').getall()
        if brand_urls:
            for url in brand_urls:
                if url and '/mobiles/' in url:
                    brand_url = self.base_url.format(url) if url.startswith('/') else url
                    if pages_processed < self.pages:
                        pages_processed += 1
                        yield scrapy.Request(url=brand_url, callback=self.parse_mobile_urls)

    def parse_mobile_urls(self, response):
        """method for parse product urls"""
        print('RESp = ', response.url)
        print('\n')
        global pages_processed
        products_data = response.css('script[id="jsonLD"]::text').get()
        try:
            json_data = json.loads(products_data)
        except:
            json_data = None
        if json_data:
            product_list = json_data.get('itemListElement')
            if product_list:
                for product in product_list:
                    item = FlipkartScraperItem()
                    item['title'] = product.get('name')
                    item['product_url'] = product.get('url')
                    try:
                        item['sku'] = item['product_url'].split('/')[3]
                    except:
                        item['sku'] = item['product_url']
                    if item['product_url']:
                        yield scrapy.Request(
                            url=item['product_url'], callback=self.parse_mobile_data, meta={'item': item}
                        )
                pages_processed += 1
                next_page = response.css('a[class="_1LKTO3"]::attr(href)').get()
                if next_page:
                    if pages_processed < self.pages:
                        next_page_url = self.base_url.format(next_page)
                        print('NP + ', next_page_url, '\n')
                        if next_page_url:
                            yield scrapy.Request(next_page_url, callback=self.parse_mobile_urls)

    def parse_mobile_data(self, response):
        """method for get product details"""
        item = response.meta.get('item')
        item['title'] = response.css('span[class="B_NuCI"]::text').get()
        item['offer_price'] = response.css('div[class="_30jeq3 _16Jk6d"]::text').get()
        list_price = response.css('div[class="_3I9_wc _2p6lqe"]::text').getall()
        item['list_price'] = ''.join(list_price) if list_price else item['offer_price']
        item['colour'] = response.css('div[class="_3Oikkn _3_ezix _2KarXJ"]::text').get()
        script_data = response.css('script[id="jsonLD"]::text').get()
        try:
            json_form = json.loads(script_data)[0]
        except:
            json_form = None
        item['brand'] = json_form.get('brand', {}).get('name', {}) if json_form.get('brand') else None
        storage = response.css('a[class="_1fGeJ5 PP89tw"]::text').getall()
        item['rom'] = storage[0] if storage else None
        item['ram'] = storage[1] if storage and len(storage) > 1else None
        processor_data = response.css('li[class="_21Ahn-"]::text').getall()
        item['processor'] = processor_data[-1] if processor_data else None
        item['image_url'] = response.css('div[class="CXW8mj _3nMexc"] img::attr(src)').get()
        item['description'] = ', '.join(processor_data) if processor_data else None
        yield item
