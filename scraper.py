from bs4 import BeautifulSoup
import requests
import scrapy
from scrapy.http import HtmlResponse
from scrapy.selector import Selector

BASE_URL = 'https://dgap.de'

XPATH_FIRST_PAGE = '//*[contains(concat( " ", @class, " " ), concat( " ", "left_col", " " ))]'
XPATH_LIST_RESULTS = '//a[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]//img | //*[contains(concat( " ", @class, " " ), concat( " ", "content_text", " " ))]//a'
XPATH_LIST_HEADLINES = '//*[contains(concat( " ", @class, " " ), concat( " ", "content_text", " " ))]//a'
XPATH_ENGLISH_NEWS = '//*[contains(concat( " ", @class, " " ), concat( " ", "icons", " " ))]//*[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]//img'
START_URL = 'https://dgap.de/dgap/News/?newsType=ADHOC&page=1&limit=20'
page = requests.get(START_URL)
soup = BeautifulSoup(page.content, 'html.parser')
x = Selector(response=page).xpath(XPATH_LIST_HEADLINES)
headlines_links = [href.xpath('@href').extract()[0] for href in x]

XPATH_SYMBOLS_ENG = '//a[(((count(preceding-sibling::*) + 1) = 4) and parent::*)]'

eng_links = Selector(response=page).xpath(XPATH_SYMBOLS_ENG)
headlines_links_eng = [href.xpath('@href').extract()[0] for href in eng_links if 'newsID' in href.xpath('@href').extract()[0]]

## Extract company metadata and text
XPATH_COMPANY_NAME = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "darkblue", " " ))]'
XPATH_COMPANY_META = '//*[contains(concat( " ", @class, " " ), concat( " ", "darkblue", " " ))] | //*[(@id = "content")]//ul'
XPATH_COMPANY_WKN_ISIN_COUNTRY = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//ul'
XPATH_COMPANY_WKN = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//li[(((count(preceding-sibling::*) + 1) = 1) and parent::*)]'
XPATH_COMPANY_ISIN = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//li[(((count(preceding-sibling::*) + 1) = 2) and parent::*)]'
XPATH_COMPANY_COUNTRY = '//*[contains(concat( " ", @class, " " ), concat( " ", "company_header", " " ))]//li[(((count(preceding-sibling::*) + 1) = 3) and parent::*)]'
response = requests.get(BASE_URL+headlines_links_eng[0]) # HtmlResponse(url = BASE_URL+headlines_links_eng[0])
test = Selector(response=response)#.xpath(XPATH_COMPANY_ISIN)
company_meta_data = {}
test.xpath("text()").extract()
company_meta = test.extract()[0]
import re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

company_meta = ' '.join(remove_tags(company_meta).split())
company_meta.split('Land: ')

pattern = r'(ISIN): (.+)[\s]'
re.findall(pattern,company_meta)
