import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging


def r(nameOfModule):
    import importlib
    importlib.reload(nameOfModule)
    print("{} reloaded.".format(nameOfModule))


class shopeeSpider:
    def __init__(self, saving=False):
        self.headers = None

    # Main Method.
    def search(self, keyword, limit=9999, proxy=None):
        self.headers = self.structured_headers_and_keywords(keyword)

        raw_items = []
        total_count = 0
        from_item = 0

        # Fetch Items
        while True:
            fetched_items, total_count = self.fetch_items(
                keyword=keyword,
                newest=from_item
            )
            raw_items += fetched_items

            if self.already_fetehed_all(from_item, total_count, limit):
                break
            else:
                from_item += 50
        # Formating
        formated_items = []
        for item in raw_items:
            formated_items.append(
                self.get_formated_item_dict(item, keyword)
            )
        return formated_items

    def fetch_items(self, keyword="marshall stockwell", newest=0, limit=9999):

        formatted_link = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={keyword}&limit=50&newest={newest}&order=desc&page_type=search&version=2'.format(
            keyword=keyword,
            newest=newest
        )
        req = requests.get(formatted_link, headers=self.headers)
        response = req.json()
        items = response['items']

        total_count = response['total_count']
        print("[fetch_items()] <{}> {}/{} items".format(
            str(req.status_code),
            str(newest + len(items)),
            str(total_count)))
        return items, total_count

    def already_fetehed_all(self, from_item, total_count, limit):
        return from_item + 50 > total_count or from_item + 50 > limit

    def get_formated_item_dict(self, item, keyword):
        formated_item_dict = {
            'itemid': item['itemid'],
            'shopid': item['shopid'],
            'name': item['name'],
            'item_status': item['item_status'],
            'image': item['image'],
            'images': item['images'],
            'brand': item['brand'],
            'liked_count': item['liked_count'],
            'view_count': item['view_count'],
            'stock': item['stock'],
            'price': self.formated_price(item['price']),
            'price_min': self.formated_price(item['price_min']),
            'price_max': self.formated_price(item['price_max']),
            'currency': item['currency'],
            'url': self.make_item_url(
                item['name'], item['shopid'], item['itemid']),
            'tag_name': keyword
        }
        return formated_item_dict

    def item_price_any_none(self, url, test_keyword="Marshall"):
        # TODO
        if True:
            return True
        else:
            return False

    def getHeaders(self):
        logging.debug("Execute getHeaders()")

        # Headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # driver requests, get cookie and csrf-token
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get('https://shopee.tw/')
        cookie, csrftoken = self.get_cookie_and_csrftoken(driver)
        driver.close()

        # strctured headers
        headers = {
            'cookie': cookie,
            'referer': '',  # apply in getitems()
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        return headers

    def get_cookie_and_csrftoken(self, driver):
        cookie = '; '.join(['{}={}'.format(item.get('name'), item.get(
            'value')) for item in driver.get_cookies()])
        csrftoken = ""

        for item in driver.get_cookies():
            if item.get('name') == 'csrftoken':
                csrftoken = item.get('value')

        if csrftoken == "":
            logging.warning("Not getting CSRF token.")
        return cookie, csrftoken

    def structured_headers_and_keywords(self, keyword=None):
        headers = self.getHeaders()
        keyword = keyword or "marshall stockwell"
        urllib.parse.quote(keyword)
        headers['referer'] = 'https://shopee.tw/search?keyword={}'.format(
            keyword)
        return headers

    # Helper
    def formated_price(self, item_price):
        return item_price / 100000

    def make_item_url(self, item_name, shop_id, item_id):
        # item_name = new_items[i]['name']
        # shop_id = new_items[i]['shopid']
        # item_id = new_items[i]['itemid']

        url = "{}/{}-i.{}.{}".format(
            'https://shopee.tw',
            item_name.replace(' ', '-'),
            shop_id,
            item_id
        )
        return url

    # Data Storage
    def save_to_csv(self):
        pass

    # Testing
    def test_getItems(self):
        pass

    def test_getHeaders(self):
        pass


def testHeader(headers, keyword):
    keyword = urllib.parse.quote(keyword)
    headers['referer'] = 'https://shopee.tw/search?keyword={}&page=0'.format(
        keyword)
    req = requests.get(
        'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={keyword}&limit=100&newest=0&order=desc&page_type=search&version=2'.format(keyword=keyword), headers=headers)
    response = req.json()
    items = response['items']
    prices = [i['price'] for i in items]
    return prices

# headers['']
# testHeader(headers,keyword)
