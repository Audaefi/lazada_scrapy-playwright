OT_NAME = 'lazada'

SPIDER_MODULES = ['lazada.spiders']
NEWSPIDER_MODULE = 'lazada.spiders'

ROBOTSTXT_OBEY = False

#PLAYWRIGHT_LAUNCH_OPTIONS = {"headless": False}

FEEDS = {"s3://rdata-storage/%(name)s/%(name)s_%(time)s.csv": {"format": "csv"}}

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 3

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"