import json
import pprint
from time import sleep
from datetime import datetime
from pytz import timezone
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from feedgen.feed import FeedGenerator

jst=timezone('Japan')

author = '楽天証券の投資情報メディア トウシル'

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)

def main():
    url = 'https://media.rakuten-sec.net/category/toushiru'
    print(f'Start fetching {url} ...')

    try:
        driver.get(url)

        fg = FeedGenerator()
        fg.id(url)
        fg.title(driver.title)
        fg.author( {'name': driver.find_element(By.XPATH, '/html/head/meta[13]').get_attribute('content')} )
        fg.link( href = url, rel='alternate' )
        fg.logo(driver.find_element(By.XPATH, '/html/head/meta[10]').get_attribute('content'))

        articles = list(map(lambda elm: {
            'href': elm.find_element(By.CSS_SELECTOR, '.title a').get_attribute('href'),
            'title': elm.find_element(By.CSS_SELECTOR, '.title').text,
            'category': elm.find_element(By.CSS_SELECTOR, '.cname').text,
            'timestamp': elm.find_element(By.CSS_SELECTOR, '.date').text.replace('NEW ', ''),
            'eyecatch': elm.find_element(By.CSS_SELECTOR, 'img').get_attribute('data-src'),
            'description': elm.find_element(By.CSS_SELECTOR, 'img').get_attribute('alt')
        }, driver.find_elements(By.CSS_SELECTOR, '.article-list .list')))

        for article in articles:
            fe = fg.add_entry()
            fe.id(article['href'])
            fe.title(article['title'])
            fe.author({ 'name': author })
            fe.link(href=article['href'], rel='alternate')
            fe.description(article['description'])
            fe.published(datetime.strptime(article['timestamp'], '%Y/%m/%d').replace(tzinfo=jst))

        atomfeed = fg.atom_str(pretty=True)
        print(atomfeed)
        fg.atom_file('./toushiru.xml')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
