import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://books.toscrape.com/catalogue/soumission_998/index.html'
    #'https://books.toscrape.com/catalogue/soumission_998/index.html'
    #'https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'
    #'https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')

    """Return every products page url on active page 
    in the form of a list"""

    def get_all_products_url():
        products_links = []
        products = soup.findAll('h3')
        for product in products:
            a = product.find('a')
            link = a['href']
            products_links.append('https://books.toscrape.com/' + link)
        return products_links

    def get_title():
        title = soup.find('h1')
        return title.string

    def get_product_upc():
        upc = soup.find('td')
        return upc.string

    def get_price_with_tax():
        prices = soup.findAll('td')
        return prices[3].string

    def get_price_without_tax():
        prices = soup.findAll('td')
        return prices[2].string

    def get_stock():
        number_in_stock = soup.findAll('td')
        return number_in_stock[5].string

    def get_product_description():
        descriptions = soup.findAll('p')
        return descriptions[3].string

    def get_category():
        category = soup.find('ul', class_='breadcrumb').find('a', href='../category/books/historical-fiction_4'
                                                                       '/index.html')
        return category.string

    def get_rating_review():
        rating = soup.find('div', class_='col-sm-6 product_main').findAll('p')
        return rating[2]['class'][1]

    def get_img_url():
        images = soup.find('div', class_='item active')
        links = []
        #for image in images:
        a = images.find('img')
        link = a['src']
        links.append('https://books.toscrape.com/' + link)
        return links

    print(get_img_url())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
