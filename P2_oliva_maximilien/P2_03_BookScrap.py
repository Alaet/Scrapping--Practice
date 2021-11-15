import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import time
import urllib.request
import os

# region Create directory Book_Images in current script directory
current_directory = os.getcwd()

book_image_directory = os.path.join(current_directory + '/Book_images/')

csv_directory = os.path.join(current_directory + '/Export_csv/')
if not os.path.exists(book_image_directory):
    os.makedirs(book_image_directory)

if not os.path.exists(csv_directory):
    os.makedirs(csv_directory)
# endregion

# region Functions for each information, for any book's url provided

"""Parse any url given and return the result for use"""


def soup_url(given_url):
    given_url_response = requests.get(given_url)
    given_url_soup = BeautifulSoup(given_url_response.content, 'html.parser')
    return given_url_soup


"""Return URL's list for every book's url"""


def get_all_products_url(given_soup):
    books_links = []
    books_url = given_soup.findAll('h3')
    for url_book in books_url:
        a = url_book.find('a')
        link_url = a['href']
        books_links.append(("https://books.toscrape.com/" + link_url))
    return books_links


def get_product_upc(given_soup):
    given_soup_upc = given_soup.find('td')
    return given_soup_upc.string


def get_title(given_soup):
    given_soup_title = given_soup.find('h1')
    return given_soup_title.string


def get_price_with_tax(given_soup):
    given_soup_price = given_soup.findAll('td')
    return given_soup_price[3].text


def get_price_without_tax(given_soup):
    given_soup_price = given_soup.findAll('td')
    return given_soup_price[2].text


def get_stock(given_soup):
    given_soup_number_in_stock = given_soup.findAll('td')
    return given_soup_number_in_stock[5].string


def get_product_description(given_soup):
    given_soup_description = given_soup.findAll('p')
    return given_soup_description[3].string


def get_rating_review(given_soup):
    given_soup_rating_stars = given_soup.find('div', class_='col-sm-6 product_main').findAll('p')
    return given_soup_rating_stars[2]['class'][1]

"""Return Image URL from a page book"""


def get_img_url(given_soup):
    image_div = given_soup.find('div', class_='item active')
    given_soup_image_url = []
    a = image_div.find('img')
    link_url = a['src']
    given_soup_image_url.append('https://books.toscrape.com/' + link_url)
    return given_soup_image_url[0]
# endregion

# region Get every categories on main page and return every url as a list : categories_url"""


URL = "https://books.toscrape.com/index.html"
soup = soup_url(URL)
category_div = soup.find(class_='nav nav-list')
categories_urls = []
links_url = category_div.findAll('a')

for url in links_url:

    link = str(url['href'])
    categories_urls.append("https://books.toscrape.com/" + link.replace('index.html', ''))

categories_urls.pop(0)
# endregion

# region CSV environment preparation with name: [Category title + DateOfTheDay].csv

for url in categories_urls:

    """URL's category page, from list categories_urls"""
    URL_CATEGORY = url

    urls_page_category = [URL_CATEGORY + "index.html"]

    """Determine numbers of books in category to fix number of pages to search"""
    soup_category_url = soup_url(urls_page_category[0])
    div_nb = soup_category_url.find('div', class_='col-sm-8 col-md-9')
    nbs = div_nb.findAll('strong')
    NUMBER_OF_BOOKS_RESULTS = int(nbs[0].string)
    if len(nbs) > 2:
        NUMBER_OF_BOOKS_SHOWING = int(nbs[2].string)
        NUMBER_OF_PAGE = int((NUMBER_OF_BOOKS_RESULTS/NUMBER_OF_BOOKS_SHOWING) + 2)
        j = 1
    else:
        NUMBER_OF_PAGE = 1
        j = 0

    """Set CSV title based on current category"""
    title_csv = get_title(soup_category_url) + " " + date.today().strftime("%b-%d-%Y") + ".csv"
    en_tete = ["TITRE", "PRODUCT_PAGE_URL", "UPC", "PRICE_INCLUDING_TAX", "PRICE_EXCLUDING_TAX", "NUMBER_AVAILABLE",
                        "PRODUCT_DESCRIPTION", "REVIEW_RATING", "IMAGE_URL"]

    # region CSV file creation, completion
    with open(
            (os.path.join(csv_directory, title_csv)), 'a+', encoding='utf-8', newline='') as fichier_csv:
        # Create CSV file
        urls_response = []
        urls_book = []
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        writer.writerow("")
        print("Création en cour de " + title_csv + " avec : \n\n")
        """Search for NUMBER_OF_PAGE variable (determined by variables NUMBER set by user) from this category,
        index 0 being starting url page category unless there is more than ONE page to search"""

        for i in range(j, NUMBER_OF_PAGE):
            urls_page_category.append(URL_CATEGORY + "page-" + str(i) + ".html")
            urls_response = requests.get(urls_page_category[i])
            if urls_response.ok:
                soup = BeautifulSoup(urls_response.content, 'html.parser')
                urls_book = get_all_products_url(soup)  # Return all urls book from each page NUMBER_OF_PAGE
                for k in range(0, len(urls_book)):
                    book_url = "https://books.toscrape.com/catalogue/" + urls_book[k]
                    soup = soup_url(book_url)

                    """Get every informations from each book"""
                    upc = get_product_upc(soup)
                    title = get_title(soup)
                    price_with_tax = get_price_with_tax(soup)
                    price_without_tax = get_price_without_tax(soup)
                    stock = get_stock(soup)
                    description = get_product_description(soup)
                    rating_stars = get_rating_review(soup)
                    image_url = get_img_url(soup)

                    """Add every information for each book to urls_book list from book_url"""
                    urls_book[k] = [title, book_url, upc, price_with_tax, price_without_tax, stock, description,
                                    rating_stars, image_url]

                    """Save image from url"""
                    urllib.request.urlretrieve(image_url.replace("../../", ''), os.path.join(book_image_directory,
                                                                                             (title.replace(":", '')
                                                                                              .replace('.', '')
                                                                                              .replace('?', '')
                                                                                              .replace('/', '')
                                                                                              .replace('"', '')
                                                                                              .replace('*', '')
                                                                                              + '.jpg')))
                    print(title)
                    time.sleep(1)
                for row in urls_book:
                    writer.writerow(row)

                print("End of Page " + str(i) + "\n\n")
                time.sleep(1)
            else:
                pass
        print(title_csv + " a bien été extrait.")
    # endregion
# endregion
