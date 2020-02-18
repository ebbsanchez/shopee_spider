import requests
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def r(nameOfModule):
    import importlib
    importlib.reload(nameOfModule)


def getHeaders():
    chrome_options = Options()  # 啟動無頭模式
    chrome_options.add_argument('--headless')  # 規避google bug
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('https://shopee.tw/')
    cookie = '; '.join(['{}={}'.format(item.get('name'), item.get('value'))
                        for item in driver.get_cookies()])
    for item in driver.get_cookies():
        if item.get('name') == 'csrftoken':
            csrftoken = item.get('value')
    # csrftoken = [item.get('value') for item in driver.get_cookies() if item.get('name') == 'csrftoken'][0]
    driver.close()
    headers = {
        'cookie': cookie,
        'referer': 'https://shopee.tw/search?keyword=marshall',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    return headers


def getitems():
    # TODO: Get all items
    keyword = urllib.parse.quote('marshall stockwell')
    headers = getHeaders()
    headers['referer'] = 'https://shopee.tw/search?keyword={}'.format(keyword)
    all_items = []
    total_count = 0
    from_item = 0
    while True:
        formatted_link = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={keyword}&limit=50&newest={from_item}&order=desc&page_type=search&version=2'.format(
            keyword=keyword, from_item=from_item)
        req = requests.get(formatted_link, headers=headers)
        response = req.json()
        items = response['items']
        all_items += items
        total_count = response['total_count']
        if from_item + 50 > total_count:
            break
        else:
            from_item += 50

    print("[getitems()] "+'<' + str(req.status_code) + '> ',
          '{}/{} items'.format(str(from_item+len(items)), str(total_count)))
    return all_items


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
