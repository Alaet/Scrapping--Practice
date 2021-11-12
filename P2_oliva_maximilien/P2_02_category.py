import requests
from bs4 import BeautifulSoup
import csv

"""URL's category page"""
URL = "https://books.toscrape.com/catalogue/category/books/travel_2/"  # !! no index.html on URL variable !!
urls_page = [URL + "index.html"]
#  https://books.toscrape.com/catalogue/category/books/sequential-art_5/
#  https://books.toscrape.com/catalogue/category/books/historical-fiction_4/
#  https://books.toscrape.com/catalogue/category/books/travel_2/

NUMBER_OF_PAGE = 1  # Number of page searched + 1
j = 0
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


def get_price_with_tax(soup):
    prices = soup.findAll('td')
    return prices[3].text


def get_price_without_tax(soup):
    prices = soup.findAll('td')
    return prices[2].text


def get_stock(soup):
    number_in_stock = soup.findAll('td')
    return number_in_stock[5].string


def get_product_description(soup):
    descriptions = soup.findAll('p')
    return descriptions[3].string


def get_rating_review(soup):
    rating = soup.find('div', class_='col-sm-6 product_main').findAll('p')
    return rating[2]['class'][1]


def get_img_url(soup):
    images = soup.find('div', class_='item active')
    links = []
    a = images.find('img')
    link = a['src']
    links.append('https://books.toscrape.com/' + link)
    return links[0]

if NUMBER_OF_PAGE > 1:
    j = 1
soup_title = soup_url(urls_page[0])
title_csv = get_title(soup_title)
en_tete = ["TITRE", "PRODUCT_PAGE_URL", "UPC", "PRICE_INCLUDING_TAX", "PRICE_EXCLUDING_TAX", "NUMBER_AVAILABLE",
                    "PRODUCT_DESCRIPTION", "CATEGORY", "REVIEW_RATING", "IMAGE_URL"]
with open(title_csv+".csv", 'a+', encoding='utf-8', newline='') as fichier_csv:  # Create CSV file
    urls_reponse = []
    urls = []
    writer = csv.writer(fichier_csv, delimiter=',')

    """Search for NUMBER_OF_PAGE from this category, index 0 being starting url page category"""
    for i in range(j, NUMBER_OF_PAGE):
        writer.writerow(en_tete)
        writer.writerow("")
        urls_reponse = urls_page.append(URL + "page-" + str(i) +
                                        ".html")
        urls_reponse = requests.get(urls_page[i])
        if urls_reponse.ok:
            soup = BeautifulSoup(urls_reponse.content, 'html.parser')
            urls = get_all_products_url(soup)
            soup = soup_url(urls_page[i])
            for i in range(0, len(urls)):
                items_url = "https://books.toscrape.com/catalogue/" + urls[i]
                print(urls[i])
                soup = soup_url(items_url)
                upc = get_product_upc(soup)
                categories_url = get_category(soup)
                titles = get_title(soup)
                price_with_tax = get_price_with_tax(soup)
                price_without_tax = get_price_without_tax(soup)
                stock = get_stock(soup)
                desc = get_product_description(soup)
                rating = get_rating_review(soup)
                image = get_img_url(soup)
                #ligne = [url, upc, title, price_with_tax, price_without_tax, stock, desc, category, rating, image]
                urls[i] = [titles, items_url, upc, price_with_tax, price_without_tax, stock, desc, categories_url,
                           rating, image]
            for row in urls:
                writer.writerow(row)
        else:
            pass
