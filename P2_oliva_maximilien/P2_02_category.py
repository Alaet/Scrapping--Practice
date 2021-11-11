import requests
from bs4 import BeautifulSoup
import csv

"""URL's category page"""
URL = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/"  # !! no index.html on URL variable !!
urls_page = [URL + "index.html"]
#https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html
"""CATEGORY will determine the name of CSV file"""
CATEGORY = "Fiction"

NUMBER_OF_PAGE = 10  # Number of page we will search in
"""Pick up avery product link on given parsed URL page from BeautifoulSoup"""

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


def get_category(urls):
    #soup = soup_url(urls)
    #url_reponse = requests.get(urls)
    #soup = BeautifulSoup(url_reponse.content, 'html.parser')
    categories = soup.find('ul', class_='breadcrumb').findAll('a')
    return categories[2].string

def get_title(urls):
    #url_reponse = requests.get(urls)
    #soup = BeautifulSoup(url_reponse.content, 'html.parser')
    title = soup.find('h1')
    return title.string

with open(CATEGORY+".csv", 'a+', newline='') as fichier_csv:  # Create CSV file
    urls_reponse = []
    urls = []
    """Search for NUMBER_OF_PAGE from this category, index 0 being starting url page category"""
    for i in range(1, NUMBER_OF_PAGE):
        urls_reponse = urls_page.append(URL + "page-" + str(i) +
                                        ".html")
        urls_reponse = requests.get(urls_page[i])
        if urls_reponse.ok:
            soup = soup_url(urls_page[i])
            #soup = BeautifulSoup(urls_reponse.content, 'html.parser')
            urls = get_all_products_url(soup)
            writer = csv.writer(fichier_csv, delimiter=',')
            for i in range(len(urls)):
                items_url = "https://books.toscrape.com/catalogue/" + urls[i]
                soup = soup_url(items_url)
                categories_url = get_category(soup)
                titles = get_title(soup)
                urls[i] = [items_url, categories_url, titles]
            for row in urls:
                writer.writerow(row)
        else:
            pass
