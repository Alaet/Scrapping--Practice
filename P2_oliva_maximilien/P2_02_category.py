import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

"""URL's category page,    !SET BY USER!  """
URL_CATEGORY = "https://books.toscrape.com/catalogue/category/books/travel_2/"  # !! NO INDEX.HTML ON URL VARIABLE !!


"""Variables that will determine how many page to search,    !SET BY USER!  """
NUMBER_OF_BOOKS_RESULTS = 11
NUMBER_OF_BOOKS_SHOWING = 0


"""Pick up avery product link on given parsed URL page from BeautifulSoup"""

# region All functions for each informations
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
# endregion

# region CSV environment preparation with name: [Category title + DateOfTheDay].csv


urls_page_category = [URL_CATEGORY + "index.html"]
if NUMBER_OF_BOOKS_SHOWING != 0:
    NUMBER_OF_PAGE = int((NUMBER_OF_BOOKS_RESULTS/NUMBER_OF_BOOKS_SHOWING) + 2)
    j = 1
else:
    NUMBER_OF_PAGE = 1
    j = 0

soup_title = soup_url(urls_page_category[0])
title_csv = get_title(soup_title) + " " + date.today().strftime("%b-%d-%Y")
en_tete = ["TITRE", "PRODUCT_PAGE_URL", "UPC", "PRICE_INCLUDING_TAX", "PRICE_EXCLUDING_TAX", "NUMBER_AVAILABLE",
                    "PRODUCT_DESCRIPTION", "REVIEW_RATING", "IMAGE_URL"]
# endregion

# region CSV file creation, completion
with open(title_csv+".csv", 'a+', encoding='utf-8', newline='') as fichier_csv:  # Create CSV file
    urls_reponse = []
    urls = []
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(en_tete)
    writer.writerow("")
    """Search for NUMBER_OF_PAGE from this category, index 0 being starting url page category"""
    for i in range(j, NUMBER_OF_PAGE):
        urls_reponse = urls_page_category.append(URL_CATEGORY + "page-" + str(i) + ".html")
        urls_reponse = requests.get(urls_page_category[i])
        if urls_reponse.ok:
            soup = BeautifulSoup(urls_reponse.content, 'html.parser')
            urls = get_all_products_url(soup)
            soup = soup_url(urls_page_category[i])
            for i in range(0, len(urls)):
                items_url = "https://books.toscrape.com/catalogue/" + urls[i]
                print(urls[i])
                soup = soup_url(items_url)
                upc = get_product_upc(soup)
                titles = get_title(soup)
                price_with_tax = get_price_with_tax(soup)
                price_without_tax = get_price_without_tax(soup)
                stock = get_stock(soup)
                desc = get_product_description(soup)
                rating = get_rating_review(soup)
                image = get_img_url(soup)
                urls[i] = [titles, items_url, upc, price_with_tax, price_without_tax, stock, desc, rating, image]
            for row in urls:
                writer.writerow(row)
        else:
            pass
# endregion
