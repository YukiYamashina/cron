import os
import json
import pprint
import requests
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

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)

def main():
    url = 'https://www.amazon.co.jp/b/?ie=UTF8&node=3251934051'
    # print(f'Start fetching {url} ...')

    try:
        driver.get(url)
        item_selector = '#anonCarousel1 > ol > li'
        images = list(map(lambda elm: elm.find_element(By.CSS_SELECTOR, 'img').get_attribute('src'), driver.find_elements(By.CSS_SELECTOR, item_selector)))
        items = list(map(lambda elm: {
            'href': elm.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'),
            'title': elm.find_element(By.CSS_SELECTOR, 'img').get_attribute('alt'),
            'thumbnail': elm.find_element(By.CSS_SELECTOR, 'img').get_attribute('src'),
        }, driver.find_elements(By.CSS_SELECTOR, item_selector)))

        item_data = {
            'postToken': os.environ.get('LINE_POST_TOKEN'),
            'type': 'image',
            'imageUrls': images
        }
        with open('./kindle.json', 'w') as f:
            json.dump(items, f, indent=4, ensure_ascii=False)

        requests.post(os.environ.get('LINE_POST_API_URL'), json=item_data)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
