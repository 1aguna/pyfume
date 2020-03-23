from selenium import webdriver
from bs4 import BeautifulSoup
from seleniumwire import webdriver
import time
from lxml import html
from lxml import etree
import re

with open("links.txt", "r") as inf:
        perfume_urls = inf.readlines()

with open("perfumes.txt", "w") as outf:
    browser = webdriver.Firefox()

    for url in perfume_urls:
        browser.get(url)

        soup = BeautifulSoup(browser.page_source, 'lxml')
        tree = etree.HTML(str(soup))

        results = soup.find_all('a', id=re.compile('^o_perfumetooltip'))

        for res in results:
            # print(res['href'])
            outf.write(str(res['href']) + "\n")
