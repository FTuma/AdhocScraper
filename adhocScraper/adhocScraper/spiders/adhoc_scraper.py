# -*- coding: utf-8 -*-
import re
from datetime import datetime

import scrapy
from adhocScraper.items import AdhocNewsItem
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags


class AdhocScraperSpider(scrapy.Spider):
    name = 'adhoc_scraper'
    allowed_domains = ['dgap.de']

    XPATH_SYMBOLS_ENG = '//a[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]'
    XPATH_SECOND_PAGE = '//*[@id="content"]/div[1]/div/div[2]/a'
    XPATH_NEXT_PAGE = '//*[@id="content"]/div[1]/div/div[2]/div[2]/a'

    XPATH_COMPANY_NAME = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]\
    //*[contains(concat( " ", @class, " " ), concat( " ", "darkblue", " " ))]'
    XPATH_COMPANY_WKN_ISIN_COUNTRY = '//*[@id="content"]/div[1]/div[1]/ul/li'
    XPATH_COMPANY_DATETIME = '//*[contains(concat( " ", @class, " " ), concat( " ", "news_content", " " ))]\
    //*[contains(concat( " ", @class, " " ), concat( " ", "darkblue", " " ))]'
    XPATH_COMPANY_HEADLINE = '//*[@id="content"]/div[1]/div[2]/div/div/h1'
    XPATH_COMPANY_MAINTEXT = '//*[contains(concat( " ", @class, " " ), concat( " ", "news_main", " " ))]'
    XPATH_COMPANY_MAINTEXT_PRE = '//pre'
    XPATH_COMPANY_MAINTEXT_BREAKWORDS = '//*[contains(concat( " ", @class, " " ), concat( " ", "break-word", " " ))]'
    XPATH_COMPANY_MAINTEXT_X = ''
    RE_DATETIME = r'.+ (\d\d\.\d\d\.\d\d\d\d \| \d\d:\d\d)'

    # TODO: Stop at last stored newsID & cleanup

    def __init__(self, url='https://dgap.de/dgap/News/?newsType=ADHOC&page=1&limit=20', *args, **kwargs):
        super(AdhocScraperSpider, self).__init__(*args, **kwargs)
        # Set the start_urls to be the one given in url parameters
        self.start_urls = [url]

    def parse(self, response):
        href_selectors = response.xpath(self.XPATH_SYMBOLS_ENG)
        for selector in href_selectors:
            link = selector.xpath('@href').extract()[0] if 'newsID' in selector.xpath('@href').extract()[0] else False
            if link:
                request = response.follow(link, callback=self.parse_adhoc_page)
                yield request
            else:
                continue
        if response.url != self.start_urls[0]:
            next_page_selector = response.xpath(self.XPATH_NEXT_PAGE)
        else:
            next_page_selector = response.xpath(self.XPATH_SECOND_PAGE)

        link_next_page = next_page_selector.xpath('@href').extract_first()
        request = response.follow(link_next_page, callback=self.parse)
        yield request

    def parse_adhoc_page(self, response):
        l = ItemLoader(item=AdhocNewsItem(), response=response)
        l.add_value('newsID', re.search(r'.*newsID=(\d+)', response.url).group(1))
        l.add_value('companyID', re.search(r'.*companyID=(\d+)', response.url).group(1))

        l.add_value('url', response.url)
        l.add_xpath('company_name', self.XPATH_COMPANY_NAME)

        company_meta = [' '.join(remove_tags(x).split()) for x in
                        response.xpath(self.XPATH_COMPANY_WKN_ISIN_COUNTRY).extract()]
        if 'WKN' in company_meta[0]:
            l.add_value('wkn', re.search(r'WKN: (.+)', company_meta[0]).group(1))
            l.add_value('isin', re.search(r'ISIN: (.+)', company_meta[1]).group(1))
            l.add_value('country', re.search(r'Land: (.+)', company_meta[2]).group(1))
        else:
            l.add_value('wkn', '')
            l.add_value('isin', re.search(r'ISIN: (.+)', company_meta[0]).group(1))
            l.add_value('country', re.search(r'Land: (.+)', company_meta[1]).group(1))

        ts_string = response.xpath(self.XPATH_COMPANY_DATETIME).re_first(self.RE_DATETIME, default='', )
        l.add_value('timestamp', datetime.strptime(ts_string, "%d.%m.%Y | %H:%M"))
        l.add_xpath('headline', self.XPATH_COMPANY_HEADLINE)
        # Different XPATHs are used for the main text, therefore try all of them
        l.add_xpath('text', self.XPATH_COMPANY_MAINTEXT)
        l.add_xpath('text', self.XPATH_COMPANY_MAINTEXT_PRE)
        l.add_xpath('text', self.XPATH_COMPANY_MAINTEXT_BREAKWORDS)

        return l.load_item()
