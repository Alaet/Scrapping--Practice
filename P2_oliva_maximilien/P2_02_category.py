import requests
from bs4 import BeautifulSoup
import csv

"""URL's category page"""
URL = "https://books.toscrape.com/catalogue/category/books/historical-fiction_4/"  # !! no index.html on URL variable !!
urls_page = [URL + "index.html"]
#https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html
#https://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html


NUMBER_OF_PAGE = 10  # Number of page searched
"""Pick up avery product link on given parsed URL page from BeautifulSoup"""


def soup_url(url):
    url_reponse = requests.get(url)
    soup = BeautifulSoup(url_reponse.content, 'html.parser')
    return soup


def get_all_products_url(soup):
    products_links = []
    products = soup.findAll('h3')
    for product in products:
        a = product.find('a')
        link = a['href']
        products_links.append(("https://books.toscrape.com/" + link))
    return products_links

def get_product_upc(soup):
    upc = soup.find('td')
    return upc.string

def get_category(soup):
    categories = soup.find('ul', class_='breadcrumb').findAll('a')
    return categories[2].string


def get_title(soup):
    title = soup.find('h1')
    return title.string


print(urls_page[0])
soup_title = soup_url(urls_page[0])
title_csv = get_title(soup_title)
with open(title_csv+".csv", 'a+', newline='') as fichier_csv:  # Create CSV file
    urls_reponse = []
    urls = []
    """Search for NUMBER_OF_PAGE from this category, index 0 being starting url page category"""
    for i in range(1, NUMBER_OF_PAGE):
        urls_reponse = urls_page.append(URL + "page-" + str(i) +
                                        ".html")
        urls_reponse = requests.get(urls_page[i])
        if urls_reponse.ok:
            soup = soup_url(urls_page[i])
            urls = get_all_products_url(soup)
            writer = csv.writer(fichier_csv, delimiter=',')
            for i in range(len(urls)):
                items_url = "https://books.toscrape.com/catalogue/" + urls[i]
                soup = soup_url(items_url)
                upc = get_product_upc(soup)
                categories_url = get_category(soup)
                titles = get_title(soup)
                #ligne = [url, upc, title, price_with_tax, price_without_tax, stock, desc, category, rating, image]
                urls[i] = [titles, items_url, upc, categories_url]
            for row in urls:
                writer.writerow(row)
        else:
            pass
