from selenium import webdriver
from bs4 import BeautifulSoup
from seleniumwire import webdriver
import time
from lxml import html
from lxml import etree


with open("links.txt", "w") as f:
    browser = webdriver.Firefox()
    browser.get("https://www.parfumo.net/Popular_Brands")

    soup = BeautifulSoup(browser.page_source, 'lxml')
    tree = etree.HTML(str(soup))

    res_set = soup.find_all('div', class_="list-col-3")

    for res in res_set:
        link = res.find('a')['href']
        f.write(str(link) + "\n")
