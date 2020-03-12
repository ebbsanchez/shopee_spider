import requests
import pandas as pd
import logging
import json
from datetime import datetime
import math
import multiprocessing as mp
import re
import random

import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ProxyCollector:
    def __init__(self, filename, dont_init=False, timeout=10):
        self.filename = 'datasets/{}.csv'.format(filename)
        self.columns = ["ip:port", 'status',
                        'status_for_projects', 'updated_time']
        self.proxies_df = pd.DataFrame(columns=self.columns)
        self.proxies_on_call = []
        self.timeout = timeout
        
        # for shopee testing
        self.headers = None
        self.keyword = None

        if not dont_init:
            self.init_df()
        else:
            logging.warning(
                ' Not loading old data. Will get clean DataFrame and it might overwrite the old {}.csv. Make sure you are using clean file for testing.'.format(self.filename))
        logging.debug("timeout set to {} secs.".format(self.timeout))

    def init_df(self):
        logging.debug("[init] Loading {}...".format(self.filename))
        try:
            with open(self.filename, 'rb') as f:
                self.proxies_df = pd.read_csv(self.filename)
            logging.info("[init] {} loaded.".format(self.filename))
        except FileNotFoundError as e:
            logging.info(
                "[init] {} not found. get clean DataFrame... the file not exists and directory need to be created.".format(self.filename))

    def collect_raw_proxies_async(self, url):
        logging.info("Collecting from {}".format(url))
        raw_proxy_list = self.get_proxy_from_git_content(url)
        count = 0
        result = []
        for small_list in self.listsep_gen(raw_proxy_list, limit=8):
            status_and_proxy = self.testing_proxies_async(small_list)
            result += status_and_proxy
            for status, proxy in status_and_proxy:
                count += 1
                logging.info("[{}]{}: {}".format(count, proxy, status))
                if status == True:
                    self.add_proxy(proxy, status="alive")

        return result

    def testing_proxies_async(self, proxies, processes=mp.cpu_count()):
        logging.debug("Start testing proxies async")
        status_and_proxy = []
        p = mp.Pool(processes=processes)
        result = p.map(self.check_proxy_alive, proxies)
        p.close()
        p.join()
        for index, status in enumerate(result):
            status_and_proxy.append((status, proxies[index]))

        return status_and_proxy

    def listsep_gen(self, biglist, limit=10):
        small_list = []
        for item in biglist:
            small_list.append(item)
            if len(small_list) >= limit:
                yield small_list
                small_list = []
        yield small_list

    def get_proxy_from_git_content(self, url, limit=None):
        proxy_list = []
        lines = requests.get(url).text.split('\n')
        count = 0
        for line in lines:
            if self.valid_proxy_url(line):
                proxy_list.append(line)
                count += 1
            if limit != None and count >= limit:
                break
        return proxy_list

    def check_proxy_alive(self, proxy, timeout=None):
        if timeout == None:
            timeout = self.timeout
        logging.debug("Testing {}...".format(proxy))
        try:
            ip = self.get_my_ip(proxy=proxy, timeout=timeout)
            logging.info(' Proxy worked. IP: {}'.format(ip))
            # self.add_proxy(proxy, status='alive')
            return True
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout) as e:
            logging.info(' {} proxy not working...'.format(proxy))
            return False
        except requests.exceptions.ConnectionError as e:
            logging.info("ConnectionError, skip this proxy.")
            return False
        except requests.exceptions.InvalidProxyURL as e:
            logging.info("Not a valid proxy url. Assume is the end of file.")
            return False

    def get_my_ip(self, proxy=None, timeout=None):
        if timeout == None:
            timeout = self.timeout
        # """NOTE: Proxy need to be full path (http://xxx.xxx.xxx.xxx:xxxx) """
        if proxy == None:
            pass
        else:
            proxy = self.format_proxy_with_http(proxy)
            proxy = {
                'http': proxy,
                'https': proxy,
            }
        req = requests.get('https://api.ipify.org?format=json',
                           proxies=proxy, timeout=timeout)
        req_json = json.loads(req.text)
        logging.debug("My {} is: {}".format('IP', req_json['ip']))
        return req_json['ip']

    def format_proxy_with_http(self, proxy):
        logging.debug("proxy= {}".format(proxy))

        if proxy.startswith('http://'):
            return proxy
        else:
            return "http://{}".format(proxy)


    def add_proxy(self, proxy, status="", status_for_projects="", save=True):

        old_proxies = self.proxies_df['ip:port'].to_list()
        now_time = datetime.strftime(datetime.now(), '%Y-%m-%d')

        if not (proxy in old_proxies):
            logging.info("[Add Proxy] New proxy Addedd: {}.".format(proxy))
            if status == "":
                status = 'unknown'
            if status_for_projects == "":
                status_for_projects = 'unknown'

            new_proxies = pd.DataFrame(
                [[proxy, status, status_for_projects, now_time]], columns=self.columns)
            self.proxies_df = self.proxies_df.append(
                new_proxies, ignore_index=True)
        else:
            logging.info("[Add Proxy] Knowned proxy. Updated.")
            if status == "":
                status_series = self.proxies_df.loc[self.proxies_df['ip:port']== proxy, "status"]
                try:
                    status = status_series.item()
                except ValueError as e:
                    if len(status_series) > 1:
                        self.clean_duplicated_proxy(proxy)
                        logging.warning(
                            "[!!!]Find Duplicated proxy.. cleaning duplicated.. but somewhere must to get fixed.")
                        status_series = self.proxies_df.loc[self.proxies_df['ip:port']== proxy, "status"]
                        status = status_series.item()
                    else:
                        raise ValueError

            if status_for_projects == "":
                status_for_projects_series = self.proxies_df.loc[self.proxies_df['ip:port']== proxy, "status_for_projects"]
                try:
                    status_for_projects = status_for_projects_series.item()
                except ValueError as e:
                    if len(status_for_projects_series) > 1:
                        self.clean_duplicated_proxy(proxy)
                        logging.warning(
                            "[!!!]Find Duplicated proxy.. cleaning duplicated.. but somewhere must to get fixed.")
                        status_for_projects_series = self.proxies_df.loc[
                            self.proxies_df['ip:port'] == proxy, "status_for_projects"]
                        status_for_projects = status_for_projects_series.item()
                    else:
                        raise ValueError

            self.proxies_df.loc[self.proxies_df['ip:port'] == proxy, [
                "status", "status_for_projects", "updated_time"]] = [status, status_for_projects, now_time]

        if save == True:
            with open(self.filename, 'w') as f:
                self.proxies_df.to_csv(f, index=False)
            logging.debug(" Add proxy and SAVED to {}.".format(self.filename))
        else:
            logging.debug(
                " Add proxy but NOT SAVING to {}.".format(self.filename))

    # User Helper
    def print_proxy_in_file(self):
        try:
            with open(self.filename, 'rb') as f:
                self.proxies_df = pd.read_csv(f)
            for index, proxy in self.proxies_df.iterrows():
                print("[*] {} is {}".format(proxy['ip:port'], proxy['status']))

        except FileNotFoundError as e:
            logging.debug(e)
            print("[*] {} not found. must be a new file? There is nothing to print.")

    def return_alive_proxy_series_list(self, test=False):
        # TODO: Test proxies before return.
        alive_proxies = []
        for index, proxy in self.proxies_df.iterrows():
            if proxy['status'] == 'alive':
                alive_proxies.append(proxy)
        return alive_proxies

    def return_proxies(self, limit=1, status="", status_for_projects=""):
        # TODO: Add 'updated_time' filter
        # QUIESTION: What if there is no proxy in DB?
        # TODO: Notify user if there is no proxy. -> It return Nan
        if status != "":
            result_df = self.proxies_df.loc[self.proxies_df['status'] == status]
        else:
            result_df = self.proxies_df.loc[self.proxies_df['status'] == "alive"]

        if status_for_projects != "":
            result_df = result_df.loc[result_df["status_for_projects"] == status_for_projects]

        result_series = result_df.sample(n=limit)['ip:port']
        result_list = result_series.to_list()

        if math.isnan(result_list[0]):
            logging.critical("There is no proxy anymore..")
            raise Exception
        else:
            return result_list

    def clean_duplicated_proxy(self, proxy):  # For bug fixing
        to_delete_df = self.proxies_df.loc[self.proxies_df['ip:port'] == proxy]
        to_delete_df = to_delete_df.sample()
        self.proxies_df = self.proxies_df.drop(to_delete_df.index[0])
        return

    def retest_old_proxies(self):
        pass



    def valid_proxy_url(self, proxy):
        reg = r"^(?:(\w+)(?::(\w+))?@)?((?:\d{1,3})(?:\.\d{1,3}){3})(?::(\d{1,5}))?$"
        if re.findall(reg, proxy):
            return True
        else:
            return False
    

    
    def return_shopee_proofed_proxies(self, keyword="Marshall", limit=10):


        self.keyword = keyword
        self.headers = self.structured_headers_and_keywords()


        logging.debug("Start testing proxies async for shopee")
        
        shopee_proofed_proxy = []
        alive_proxies = []
        count = 0

        for index, proxy in self.proxies_df.iterrows():
            # if proxy['status'] == 'alive':
            alive_proxies.append(proxy['ip:port'])


        for small_list in self.listsep_gen(alive_proxies, limit=8):
            status_and_proxy = self.testing_proxy_with_shopee_async(small_list)

            for status, proxy in status_and_proxy:
                count += 1
                logging.info("[{}]{}: {}".format(count, proxy, status))
                if status == True:
                    self.add_proxy(proxy, status="alive" ,status_for_projects="alive")
                    shopee_proofed_proxy.append(proxy)
                if len(shopee_proofed_proxy) >= limit:
                    return shopee_proofed_proxy
        return shopee_proofed_proxy



    def testing_proxy_with_shopee_async(self, proxies, processes=mp.cpu_count()):
        logging.debug("Start testing proxies async for shopee")
        status_and_proxy = []

        p = mp.Pool(processes=processes)
        result = p.map(self.check_proxy_alive_with_shopee, proxies)
        p.close()
        p.join()
        
        for index, status in enumerate(result):
            status_and_proxy.append((status, proxies[index]))

        return status_and_proxy

    def check_proxy_alive_with_shopee(self, proxy, timeout=None):
        logging.debug("Testing {}...".format(proxy))

        timeout = timeout or self.timeout

        try:

            prices = self.get_shopee_prices(proxy)

            if all(prices):
                logging.info(' Proxy worked. {}'.format(prices))
                return True
            else:
                raise requests.exceptions.ProxyError
            
        except (requests.exceptions.ProxyError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
            logging.debug(e)
            logging.info(' {} proxy not working...'.format(proxy))
            return False
        except requests.exceptions.ConnectionError as e:
            logging.debug(e)
            logging.info("ConnectionError, skip this proxy.")
            return False
        except requests.exceptions.InvalidProxyURL as e:
            logging.debug(e)
            logging.info("Not a valid proxy url. Assume is the end of file.")
            return False
    
    
    def get_shopee_prices(self, proxy=None):
        if proxy == None:
            pass
        else:
            proxy = self.format_proxy_with_http(proxy)
            proxy = {
                'http': proxy,
                'https': proxy,
            }

        prices = []
        test_link = 'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={keyword}&limit=50&newest={newest}&order=desc&page_type=search&version=2'.format(
            keyword=self.keyword,
            newest=0
        )

        req = requests.get(test_link,
                           headers=self.headers,
                           proxies=proxy,
                           timeout=self.timeout)

        response = req.json()
        items = response['items']
        for item in items:
            prices.append(item['price'])

        return prices



    def structured_headers_and_keywords(self):
        headers = self.getHeaders()
        keyword = self.keyword
        keyword = urllib.parse.quote(keyword)
        headers['referer'] = 'https://shopee.tw/search?keyword={}'.format(
            keyword)
        return headers

    def getHeaders(self):
        logging.debug("Execute getHeaders()")

        # Headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        # driver requests, get cookie and csrf-token
        driver = webdriver.Chrome(options=chrome_options)
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    proxyman = ProxyCollector(filename='proxies')
    # print('IP: {}'.format(proxyman.get_my_ip()))
    # proxyman.print_proxy_in_file()
    # a = proxyman.return_alive_proxy_series_list()
    raw_proxy_list = [
        "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt",
        "https://raw.githubusercontent.com/x-o-r-r-o/proxy-list/master/proxy-list.txt",
        "https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt",
    ]
    l = proxyman.return_shopee_proofed_proxies()
    # result = proxyman.collect_raw_proxies_async(random.choice(raw_proxy_list))
