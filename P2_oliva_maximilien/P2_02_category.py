import requests
from bs4 import BeautifulSoup
import csv

"""URL's category page"""

urls_page = ["https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"]

"""CATEGORY will determine the name of CSV file"""
CATEGORY = "Fiction"

NUMBER_OF_PAGE = 10  # Number of page we will search in
"""Pick up avery product link on given parsed URL page from BeautifoulSoup"""


def get_all_products_url(soup):
    products_links = []
    products = soup.findAll('h3')
    for product in products:
        a = product.find('a')
        link = a['href']
        products_links.append(("https://books.toscrape.com/" + link))
    return products_links


with open(CATEGORY+".csv", 'a+') as fichier_csv:  # Create CSV file
    urls_reponse = []
    urls = []
    """Search for 10 pages from this category, index 0 being starting url page category"""
    for i in range(1, NUMBER_OF_PAGE):
        urls_reponse = urls_page.append("https://books.toscrape.com/catalogue/category/books/mystery_3/page-" + str(i) +
                                        ".html")
        urls_reponse = requests.get(urls_page[i])

        if urls_reponse.ok:
            soup = BeautifulSoup(urls_reponse.content, 'html.parser')
            # for i in range(len(urls_response)):
            urls = get_all_products_url(soup)
            writer = csv.writer(fichier_csv, delimiter=',')
            for i in range(len(urls)):
                items = "https://books.toscrape.com/catalogue/" + urls[i]
                urls[i] = items
            writer.writerow(urls)
        else:
            pass
