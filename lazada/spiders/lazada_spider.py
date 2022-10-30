import scrapy
from scrapy_playwright.page import PageMethod


# from helper import should_abort_request


class LazadaSpiderSpider(scrapy.Spider):
    name = 'lazada_spider'

    custom_settings = {
        'FEEDS': {'data/%(name)s_%(time)s.csv': {'format': 'csv', }},
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': '300000'
    }

    def start_requests(self):
        keyword_list = list(map(str, input('Search Keywords : ').split(',')))
        pages = int(input("Max Crawl Pages : "))

        for keyword in keyword_list:
            for page in range(1, int(pages)+1):
                search_url = f"https://www.lazada.com.my/catalog/?_keyori=ss&from=input&page={page}&q={keyword}"
                yield scrapy.Request(
                    url=search_url,
                    callback=self.parse,
                    meta={"playwright": True,
                          "playwright_page_methods": [
                              PageMethod("wait_for_selector", '[data-tracking="product-card"]'),
                          ],
                          },
                )

    def parse(self, response):
        products_selector = response.css('[data-tracking="product-card"]')

        for product in products_selector:
            link = response.urljoin(product.xpath('.//a[text()]/@href').get())
            yield scrapy.Request(link, callback=self.parse_product, meta={"playwright": False})

        '''
        for page in range(2, int(pages) + 1):
            search_url = f"https://www.lazada.com.my/catalog/?_keyori=ss&from=input&page={page}&q=ipad"
            yield response.follow(search_url)
        '''

    def parse_product(self, response):
        yield {
            "product_href": response.request.url,
            "product_src": response.css('.div.gallery-preview-panel > div > img::attr(src)').get(),
            'product_title': response.css('.pdp-mod-product-badge-title ::Text').get(),
            'product_price': response.css('.pdp-price_color_orange ::Text').get(),
            'product_seller': response.css('.pdp-link.pdp-link_size_l.pdp-link_theme_black.seller-name__detail-name ::Text').get()
        }
