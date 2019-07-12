import os

import pandas as pd
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer

os.environ['SCRAPY_SETTINGS_MODULE'] = 'adhocScraper.settings'
configure_logging()
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    adhoc = pd.read_csv('/home/felix/PycharmProjects/AdhocScraper/adhocScraper/adhoc (copy).csv', index_col='timestamp')
    last_newsid = adhoc.newsID.iloc[0]
    yield runner.crawl('adhocScraper', last_newsid=last_newsid)
    adhoc_new = pd.read_csv('/home/felix/PycharmProjects/AdhocScraper/adhocScraper/adhoc.csv', index_col='timestamp')
    stocks_to_update = adhoc_new['isin'].unique()
    yield runner.crawl('arivaStocks', stock_isins=stocks_to_update)
    reactor.stop()


crawl()
reactor.run()  # the script will block here until the last crawl call is finished
