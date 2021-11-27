import requests
from bs4 import BeautifulSoup
import csv
from datetime import date

"""URL's book page,    !SET BY USER!  """
url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

"""Reach and Check user url's response, if it can't be reached, will prompt an error message in console"""
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.content, 'html.parser')
else:
    print("Impossible de joindre la page, vérifier l'URL")


# region All functions for each information

def get_title():
    title = soup.find('h1')
    return title.string


def get_product_upc():
    upc = soup.find('td')
    return upc.string


def get_price_with_tax():
    price = soup.findAll('td')
    return price[3].text


def get_price_without_tax():
    price = soup.findAll('td')
    return price[2].text


def get_stock():
    number_in_stock = soup.findAll('td')
    return number_in_stock[5].string


def get_product_description():
    description = soup.findAll('p')
    return description[3].string


def get_category():
    categorie = soup.find('ul', class_='breadcrumb').findAll('a')
    return categorie[2].string


def get_rating_review():
    rating_stars = soup.find('div', class_='col-sm-6 product_main').findAll('p')
    return rating_stars[2]['class'][1]


def get_img_url():
    image_div = soup.find('div', class_='item active')
    image_url = []
    a = image_div.find('img')
    link_url = a['src']
    image_url.append('https://books.toscrape.com/' + link_url)
    return image_url[0]


# endregion

# region CSV file creation, completion with name: [Book's title + DateOfTheDay].csv

csv_title = get_title() + " " + date.today().strftime("%b-%d-%Y")
header = ["PRODUCT_PAGE_URL", "UPC", "TITLE", "PRICE_INCLUDING_TAX", "PRICE_EXCLUDING_TAX", "NUMBER_AVAILABLE",
          "PRODUCT_DESCRIPTION", "CATEGORY", "REVIEW_RATING", "IMAGE_URL"]

"""CSV creation"""
with open(csv_title + ".csv", 'a+', encoding='utf-8') as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(header)

    title = get_title()
    image = get_img_url()
    desc = get_product_description()
    rating = get_rating_review()
    category = get_category()
    stock = get_stock()
    price_with_tax = str(get_price_with_tax())
    price_without_tax = str(get_price_without_tax())
    upc = get_product_upc()

    csv_line = [url, upc, title, price_with_tax, price_without_tax, stock, desc, category, rating, image]
    writer.writerow(csv_line)
# endregion
