# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import scrapy
from adhocScraper.items import ArivaStockItem
from scrapy.loader import ItemLoader


class ArivaStocksSpider(scrapy.Spider):
    name = 'arivaStocks'
    allowed_domains = ['ariva.de']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,  # Increase this number if you get blocked (Status code 429) and try again 24h later
        'ITEM_PIPELINES': {'adhocScraper.pipelines.ArivaFilePipeline': 100,
                           'adhocScraper.pipelines.ArivaCompanyMetaDataDuplicatesPipeline': 200,
                           'adhocScraper.pipelines.ArivaCompanyMetadataCSVPipeline': 300}
    }
    start_url = 'https://www.ariva.de/'

    REL_URL_METADATA = '/bilanz-guv#stammdaten'
    REL_URL_HISTORICALDATA = '/historische_kurse'
    CSS_PATH_META_FOUNDINGYEAR = '.stammdaten tr:nth-child(1) td'
    CSS_PATH_META_TICKER = '.stammdaten tr:nth-child(2) td'
    CSS_PATH_META_LISTINGDATE = '.stammdaten tr:nth-child(3) td'
    CSS_PATH_META_COUNTRY = '.stammdaten tr:nth-child(5) td'
    CSS_PATH_META_INDUSTRY = '.stammdaten tr:nth-child(7) td'
    CSS_PATH_META_STOCKTYPE = '.stammdaten tr:nth-child(8) td'
    CSS_PATH_META_SECTOR = '.stammdaten tr:nth-child(9) td'
    XPATH_SECURITYID = '//input[@name="secu"]'
    XPATH_EXCHANGEID = '//input[@name="boerse_id"]'

    BASE_URL_HISTORIC_PRICES = r'http://www.ariva.de/quote/historic/historic.csv'

    def start_requests(self):
        """If spider is started with option -a stock_isins=['ISIN1','ISIN2',...] it will scrape these ISINs"""
        stock_isins = getattr(self, 'stock_isins', None)
        if stock_isins is None:
            print('\nNo stock ISINs specified as parameter...\nReading in default ISIN list from settings.py...\n')
            path_stock_isins = self.settings.get('PATH_ISIN_LIST', '')
            try:
                with open(path_stock_isins) as fname:
                    stock_isins = fname.readlines()
            except FileNotFoundError:
                print(
                    "Couldn't read list of stock ISINs to crawl from {}, specified under 'PATH_ISIN_LIST' "
                    "in settings.py\nEither specify the list of ISINs as spider argument "
                    "or store them as line-separated txt file.".format(path_stock_isins))

        requests = [scrapy.Request(url=''.join([self.start_url, isin.strip()]), meta={'isin': isin.strip()},
                                   callback=self.parse) for
                    isin in stock_isins]

        for request in requests:
            yield request

    def parse(self, response):
        link = ''.join([response.url, self.REL_URL_METADATA])
        request = response.follow(link, callback=self.parse_stock_metadata)
        self.logger.info('Parse: Got successful response from {}\nNow navigating to {}'.format(response.url, link))
        request.meta['main_url'] = response.url
        request.meta['isin'] = response.meta['isin']

        yield request

    def parse_stock_metadata(self, response):
        # Extract & store metadata
        item = ItemLoader(item=ArivaStockItem(), response=response)
        item.add_value('security_name', response.meta['main_url'].rsplit(r'/', 1)[-1].encode('utf-8'))
        item.add_value('isin', response.meta['isin'])
        item.add_css('foundingyear', self.CSS_PATH_META_FOUNDINGYEAR)
        item.add_css('ticker', self.CSS_PATH_META_TICKER)
        item.add_css('listingdate', self.CSS_PATH_META_LISTINGDATE)
        item.add_css('country', self.CSS_PATH_META_COUNTRY)
        item.add_css('industry', self.CSS_PATH_META_INDUSTRY)
        item.add_css('stocktype', self.CSS_PATH_META_STOCKTYPE)
        item.add_css('sector', self.CSS_PATH_META_SECTOR)
        link = ''.join([response.meta['main_url'], self.REL_URL_HISTORICALDATA])

        request = response.follow(link, callback=self.parse_stock_prices)
        request.meta['item'] = item
        self.logger.info('Parse stock_metadata: successful response from {}\nNow navigating to {}'.format(
            response.url, link))

        yield request

    def parse_stock_prices(self, response):
        item = response.meta['item']
        secuid = response.xpath(self.XPATH_SECURITYID).attrib['value']
        item.add_value('arivaID', secuid)
        only_xetra_prices = self.settings.get('ONLY_XETRA_PRICES', False)
        exchangeid = response.xpath(self.XPATH_EXCHANGEID).attrib['value'] if not only_xetra_prices else 6
        item.add_value('exchangeID', exchangeid)
        start_date = self.settings.get('PRICES_START_DATE', '2000-01-01')
        end_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        stock_params_url = '?secu={}&boerse_id={}&clean_split=1&clean_payout=1&clean_bezug=1&min_time={}&max_time={}' \
                           '&trenner=%3B&go=Download' \
            .format(secuid, exchangeid, start_date, end_date)
        file_url = ''.join([self.BASE_URL_HISTORIC_PRICES, stock_params_url])
        item.add_value('file_urls', file_url)

        return item.load_item()
