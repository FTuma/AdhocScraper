import os
import pandas as pd
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

# Tells Scrapy where to look for settings.py and configures logging, if run from script
os.environ['SCRAPY_SETTINGS_MODULE'] = 'adhocScraper.settings'
configure_logging()
settings = get_project_settings()
runner = CrawlerRunner(settings)


@defer.inlineCallbacks
def crawl():
    # Try to read in existing adhoc announcement file to append new announcements to.
    # If no existing announcement file is found, all adhoc announcements will be downloaded (up to 2001).
    try:
        adhoc = pd.read_csv(settings['ADHOC_FILEPATH'], index_col='timestamp', parse_dates=True)
        adhoc.sort_index(inplace=True)
        old_length = len(adhoc)
        print('Number of adhoc announcements before update:', old_length)
        last_newsid = adhoc.newsID.iloc[-1]
        last_ts = pd.to_datetime(adhoc.index.dropna().get_values()[-1])
    except FileNotFoundError:
        print('No existing file with adhoc announcements found in {}\n'
              'Downloading all announcements from start...\n'.format(settings['ADHOC_FILEPATH']))
        last_newsid = 0
        old_length = 0
        last_ts = None

    yield runner.crawl('adhocScraper', last_newsid=last_newsid)
    adhoc_new = pd.read_csv(settings['ADHOC_FILEPATH'], index_col='timestamp', parse_dates=True)
    adhoc_new.sort_index(inplace=True)

    print('\nRetrieved {} new adhoc announcements \n'.format(len(adhoc_new) - old_length))
    last_ts = pd.to_datetime(adhoc_new.index.dropna().get_values()[0]) if last_ts is None else last_ts
    # Substract 30 business days from the last announcement timestamp, so that we can calculate the returns later for up
    # to 30 business days after an announcement was published.
    stocks_to_update = adhoc_new.loc[str(last_ts - pd.offsets.BDay(30, 'D')):, 'isin'].unique()
    print('Need to update {} stocks ...'.format(len(stocks_to_update)))
    print('Updating stock price data for all announcements published after {}'
          .format((last_ts - pd.offsets.BDay(30, 'D')).date()))

    yield runner.crawl('arivaStocks', stock_isins=stocks_to_update)
    reactor.stop()


crawl()
reactor.run()  # The script will block here until the last crawl call is finished
