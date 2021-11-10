import requests
from bs4 import BeautifulSoup
import csv


def main():
    url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    response = requests.get(url)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
    else:
        print("Impossible de joindre la page")

    # region All functions for each informations

    def get_title():
        title = soup.find('h1')
        return title.string

    def get_product_upc():
        upc = soup.find('td')
        return upc.string

    def get_price_with_tax():
        prices = soup.findAll('td')
        return prices[3].text

    def get_price_without_tax():
        prices = soup.findAll('td')
        return prices[2].text

    def get_stock():
        number_in_stock = soup.findAll('td')
        return number_in_stock[5].string

    def get_product_description():
        descriptions = soup.findAll('p')
        return descriptions[3].string

    def get_category():
        categories = soup.find('ul', class_='breadcrumb').findAll('a')
        return categories[2].string

    def get_rating_review():
        rating = soup.find('div', class_='col-sm-6 product_main').findAll('p')
        return rating[2]['class'][1]

    def get_img_url():
        images = soup.find('div', class_='item active')
        links = []
        a = images.find('img')
        link = a['src']
        links.append('https://books.toscrape.com/' + link)
        return links[0]

    # endregion

    csv_title = get_title()
    en_tete = ["product_page_url", "upc", "title", "price_including_tax", "price_excluding_tax", "number_available",
               "product_description", "category", "review_rating", "image_url"]
    with open(csv_title+".csv", 'a+') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        title = get_title()
        image = get_img_url()
        desc = get_product_description()
        rating = get_rating_review()
        category = get_category()
        stock = get_stock()
        price_with_tax = str(get_price_with_tax())
        price_without_tax = str(get_price_without_tax())
        upc = get_product_upc()
        url = 'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
        ligne = [url, upc, title, price_with_tax, price_without_tax, stock, desc, category, rating, image]
        writer.writerow(ligne)


if __name__ == '__main__':
    main()
