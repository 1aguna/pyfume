import requests
import time
from selenium import webdriver
import os
from bs4 import BeautifulSoup

# base_url = "https://www.fragrantica.com/perfume/Diptyque/Eau-Duelle-Eau-de-Parfum-49100.html"
# page = requepythsts.get(base_url)
# print(page)

# browser = webdriver.Firefox()
# browser.get("https://www.fragrantica.com/perfume/Diptyque/Eau-Duelle-Eau-de-Parfum-49100.html")

# rating xpath
#  /html/body/div[3]/div[3]/div/div/div[1]/div/div/div/div/div[6]/p/span[1]

# votes xpath
# /html/body/div[3]/div[3]/div/div/div[1]/div/div/div/div/div[6]/p/span[3]

url = "https://www.fragrantica.com/perfume/Diptyque/Eau-Duelle-Eau-de-Parfum-49100.html"

