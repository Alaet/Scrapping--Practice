import requests
from bs4 import BeautifulSoup
import csv
from datetime import date
import time

"""URL's category page,    !SET BY USER!  """
URL_CATEGORY = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/"

# !! NO "INDEX.HTML" ON URL_CATEGORY VARIABLE !!


# region All functions for each information


def soup_url(url):
    url_response = requests.get(url)
    soup = BeautifulSoup(url_response.content, 'html.parser')
    return soup


def get_all_products_url(soup):
    books_links = []
    book_url = soup.findAll('h3')
    for url in book_url:
        a = url.find('a')
        link_url = a['href']
        books_links.append(("https://books.toscrape.com/" + link_url))
    return books_links


def get_product_upc(soup):
    upc = soup.find('td')
    return upc.string


def get_title(soup):
    title = soup.find('h1')
    return title.string


def get_price_with_tax(soup):
    price = soup.findAll('td')
    return price[3].text


def get_price_without_tax(soup):
    price = soup.findAll('td')
    return price[2].text


def get_stock(soup):
    number_in_stock = soup.findAll('td')
    return number_in_stock[5].string


def get_product_description(soup):
    description = soup.findAll('p')
    return description[3].string


def get_rating_review(soup):
    rating_stars = soup.find('div', class_='col-sm-6 product_main').findAll('p')
    return rating_stars[2]['class'][1]


def get_img_url(soup):
    image_div = soup.find('div', class_='item active')
    image_url = []
    a = image_div.find('img')
    link_url = a['src']
    image_url.append('https://books.toscrape.com/' + link_url)
    return image_url[0]
# endregion

# region CSV environment preparation with name: [Category title + DateOfTheDay].csv


urls_page_category = [URL_CATEGORY + "index.html"]

"""Get category from url set by user to determine and set CSV file title"""

soup_title = soup_url(urls_page_category[0])
div = soup_title.find('div', class_='col-sm-8 col-md-9')
strong_tags = div.findAll('strong')
NUMBER_OF_BOOKS_RESULTS = int(strong_tags[0].string)
if len(strong_tags) > 2:
    NUMBER_OF_BOOKS_SHOWING = int(strong_tags[2].string)
    NUMBER_OF_PAGE = int((NUMBER_OF_BOOKS_RESULTS/NUMBER_OF_BOOKS_SHOWING) + 2)
    j = 1
else:
    NUMBER_OF_PAGE = 1
    j = 0
title_csv = get_title(soup_title) + " " + date.today().strftime("%b-%d-%Y") + ".csv"
header = ["TITRE", "PRODUCT_PAGE_URL", "UPC", "PRICE_INCLUDING_TAX", "PRICE_EXCLUDING_TAX", "NUMBER_AVAILABLE",
          "PRODUCT_DESCRIPTION", "REVIEW_RATING", "IMAGE_URL"]
# endregion

# region CSV file creation, completion
with open(title_csv, 'a+', encoding='utf-8', newline='') as fichier_csv:  # Create CSV file
    urls_response = []
    urls_book = []
    writer = csv.writer(fichier_csv, delimiter=',')
    writer.writerow(header)
    writer.writerow("")
    print("Création en cour de " + title_csv + " avec : \n\n")

    for i in range(j, NUMBER_OF_PAGE):
        urls_page_category.append(URL_CATEGORY + "page-" + str(i) + ".html")
        urls_response = requests.get(urls_page_category[i])
        if urls_response.ok:
            soup = BeautifulSoup(urls_response.content, 'html.parser')
            urls_book = get_all_products_url(soup)  # Return all urls book from each page NUMBER_OF_PAGE
            for k in range(0, len(urls_book)):
                book_url = "https://books.toscrape.com/catalogue/" + urls_book[k]
                soup = soup_url(book_url)

                """Get every information from each book"""
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
