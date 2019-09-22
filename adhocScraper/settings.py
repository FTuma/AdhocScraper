# -*- coding: utf-8 -*-
# Scrapy settings for adhocScraper project

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
# Obey robots.txt rules
ROBOTSTXT_OBEY = True


