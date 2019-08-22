# -*- coding: utf-8 -*-

# Scrapy settings for adhocScraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.utils.conf import closest_scrapy_cfg
from pathlib import Path

# Custom settings
BOT_NAME = 'adhocScraper'

SPIDER_MODULES = ['adhocScraper.spiders']
NEWSPIDER_MODULE = 'adhocScraper.spiders'

PROJECT_ROOT = Path(closest_scrapy_cfg()).parent
DATA_DIR = PROJECT_ROOT / 'data'
if not Path.is_dir(DATA_DIR):
    Path.mkdir(DATA_DIR, exist_ok=True)

ARIVA_METADATA_FILENAME = 'adhoc_stocks_metadata.csv'
ARIVA_METADATA_FILEPATH = DATA_DIR / ARIVA_METADATA_FILENAME

ADHOC_FILENAME = 'adhoc.csv'
ADHOC_FILEPATH = DATA_DIR / ADHOC_FILENAME

# Settings for the download of the individual stock price data for each company
PRICES_START_DATE = '2000-01-01'
ONLY_XETRA_PRICES = True
STOCKS_DIR = 'stocks' if not ONLY_XETRA_PRICES else 'stocks_xetra'
if not Path.is_dir(DATA_DIR / STOCKS_DIR):
    Path.mkdir(DATA_DIR / STOCKS_DIR, exist_ok=True)
FILES_STORE = str(DATA_DIR / STOCKS_DIR)  # Convert to str because FilesPipeline can't handle Path objects
STOCKS_FILES_PATH = DATA_DIR / STOCKS_DIR
MEDIA_ALLOW_REDIRECTS = True
FILES_EXPIRES = 0
# ArivaStocksSpider uses this list of ISIN to download stock price data if the parameter stock_isins isn't given
PATH_ISIN_LIST = DATA_DIR / 'ALL_STOCKS_ISIN.txt'

# Scrapy standard settings

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'adhocScraper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'adhocScraper.middlewares.AdhocscraperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'adhocScraper.middlewares.AdhocscraperDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


