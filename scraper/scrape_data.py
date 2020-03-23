from bs4 import BeautifulSoup
from lxml import html
from lxml import etree
import re
import requests
import csv


with open("perfumes.txt", "r") as inf:
    perfume_urls = inf.readlines()

with open("parfumo_data.csv") as c:
    flag = sum(1 for line in c)
    


with open("parfumo_data.csv", "a") as outf:
    csv_writer = csv.writer(outf)

    # header = ["brand", "name", "year" "rating", "votes", "longevity", "sillage", "accord1", "accord2"]
    # csv_writer.writerow(header)


    for url in perfume_urls[flag:]:
        
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        # Get the Brand Name and Perfume Name
        split_url = url.split("/")
        name = split_url[-1][:-1]
        name = name.replace("_", " ")
        brand = split_url[-2]

        # Get Longevity and Sillage
        results = soup.find_all('span', class_=['fill barfiller_color_dur', 'fill barfiller_color_sillage'])
        if results:
            try:
                long = float(results[0]['data-percentage'])
            except IndexError:
                long = None

            try:
                sill = float(results[1]['data-percentage'])
            except IndexError:
                sill = None

        else:
            long = None
            sill = None
        # Get the perfume's ratingyear_idx = str_list.index("released")
    
        results = soup.find('span', class_=['fill barfiller_color'])
        if results:
            rating = float(results['data-percentage'])
        else:
            rating = None

        # Get the perfumes number of votes
        vote_elem = soup.find('span', class_="lightblue")

        if vote_elem:
            string = vote_elem.text
            number = string.split()[0]
            nvotes = int(number[1:])

        else:
            nvotes = None
        
        # Get accords from description
        results = soup.find_all("span", itemprop="description")
        for a in results:
            string = a.text

        str_list = string.split()
        try:
            idx = str_list.index("scent")
            accords = str_list[idx + 2].split("-")

            accord1 = accords[0]
            try:
                accord2 = accords[1][:-1]
            except IndexError:
                accord2 = None

        except ValueError:
            accord1 = None
            accord1 = None
        # Get the year from description
        try:
            year_idx = str_list.index("released")
            year = int(str_list[year_idx + 2][:-1])
        except ValueError:
            year = None

        # Make the row for csv
        row = [brand, name, year, rating, nvotes, long, sill, accord1, accord2]
        row = ["null" if x is None else x for x in row]
        print(row)
        csv_writer.writerow(row)